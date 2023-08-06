import logging
import random
import asyncio
import re
import time
import aiohttp
from w3lib.url import canonicalize_url
from espider import USER_AGENT_LIST
from espider.request import Request
from espider.utils import PriorityQueue, headers_to_dict, cookies_to_dict, get_md5
from espider.response import Response
from inspect import isgenerator
from pprint import pprint, pformat
from espider._utils._colorlog import ColoredFormatter

try:
    from redis import Redis
except:
    pass


class Spider(object):
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '[%(log_color)s%(asctime)s%(reset)s] [%(log_color)s<%(name)s>%(levelname)8s%(reset)s] - %(log_color)s%(message)s%(reset)s'
    LOG_DATEFMT = '%Y/%m/%d %H:%M:%S'

    FILTER_TIMEOUT = 0
    FILTER_SKEY = None
    FILTER_DESTROY = True

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__
        self.headers = {'User-Agent': random.choice(USER_AGENT_LIST)}
        self.loop = asyncio.get_event_loop()
        self.queue = PriorityQueue()
        self.pipeline = self.__pipeline
        self.logger = logging.getLogger(self.name)
        self.detail = False
        self.filter = set()
        self.delay = 0

        self._max_worker = 10
        self._stop_counter = 3
        self._next_priority_index = 0
        self._count = 0
        self._count_map = {-1: 0}
        self._callback_priority_map = {}
        self._start_time = time.time()
        self._sema = asyncio.Semaphore(self._max_worker)

        self.FILTER_SKEY = self.name

    def __init_logger(self):
        self.logger.setLevel(self.LOG_LEVEL)

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        formatter = ColoredFormatter(fmt=self.LOG_FORMAT, datefmt=self.LOG_DATEFMT)
        sh.setFormatter(formatter)

        self.logger.addHandler(sh)

    @property
    def max_worker(self):
        return self._max_worker

    @max_worker.setter
    def max_worker(self, num):
        self._max_worker = num
        self._sema = asyncio.Semaphore(num)

    def start(self):
        self.prepare()
        self.loop.run_until_complete(self.__run())
        self.close()

    async def __run(self):
        self.__init_logger()
        consumer = asyncio.ensure_future(self.__downloader())
        await self.__init_queue()
        await self.queue.join()
        consumer.cancel()

        if self.filter is not None:
            try:
                if self.FILTER_DESTROY and hasattr(self.filter, 'delete'):
                    self.filter.delete(self.name)
            except Exception as e:
                self.logger.error('Destroy Redis Filter Error: {}'.format(e))

    async def __init_queue(self):
        for item in self.start_requests():
            if item: await self.queue.put(item)

    async def async_request(self, priority, req, callback, *args, **kwargs):

        if isinstance(req.__dict__.get('cookies', {}), str):
            req.__dict__['cookies'] = cookies_to_dict(req.__dict__.get('cookies'))

        if isinstance(req.__dict__.get('headers', {}), str):
            req.__dict__['headers'] = headers_to_dict(req.__dict__.get('cookies'))

        if self.delay: await asyncio.sleep(self.delay)

        try:
            async with aiohttp.request(**req.__dict__) as resp:
                data = await resp.read()
                response = Response(resp)
                response.text = data
                response.request = req
        except Exception as e:
            self.logger.exception(msg=f"Async Request Error: {e}")
        else:
            if priority not in self._count_map.keys(): self._count_map[priority] = 0
            self._count_map[priority] += 1
            self._count += 1

            running_time = time.time() - self._start_time
            msg = '{}: {} {} {} count {} {} running {:.2f}s rate {:.2f}'.format(
                priority,
                req.__dict__.get('method'),
                req.__dict__.get('url'),
                response.status_code,
                self._count_map,
                self._count,
                running_time,
                self._count / running_time,
            )

            if self.detail or response.status_code != 200:
                detail = pformat(req.__dict__).replace('\n', '\n\t\t')
                detail = re.sub('^\{', '{\n\t\t ', detail)
                detail = re.sub('\}$', '\n\t}', detail)
                msg = msg + '\n\t{}\n'.format(detail)

            self.logger.info(msg)
            await self.__process_callback(callback, response, *args, **kwargs)

    async def __process_callback(self, callback, response, *args, **kwargs):

        try:
            result = callback(response, *args, **kwargs)
        except Exception as e:
            self.logger.exception(msg='Process Callback({}) Error: {}'.format(callback.__name__, e))
        else:
            if isgenerator(result):
                for req in result:
                    if isinstance(req, tuple) and isinstance(req[1], Request):
                        await self.queue.put(req)
                    elif req and callable(self.pipeline):
                        self.pipeline(req)
            else:
                if result and callable(self.pipeline):
                    self.pipeline(result)

    async def __downloader(self):
        while self._stop_counter >= 0:
            tasks = []
            for i in range(self.max_worker):
                if not self.queue.empty():
                    with (await self._sema):
                        priority, req, callback, cb_args, cb_kwargs = await self.queue.get()

                        task = self.loop.create_task(
                            self.async_request(
                                priority, req, callback, *cb_args, **cb_kwargs
                            )
                        )
                        tasks.append(task)
                else:
                    if not tasks:
                        self._stop_counter -= 1
                    else:
                        await asyncio.gather(*tasks)
                        tasks.clear()

            if tasks:
                self._stop_counter = 3
                await asyncio.gather(*tasks)

        if hasattr(self.queue, '_finished'): self.queue._finished.set()

    def request(self, url=None, method=None, data=None, json=None, headers=None, cookies=None, callback=None,
                cb_args=None, cb_kwargs=None, priority=None, allow_redirects=True, **kwargs):

        if not callback: callback = self.parse

        # 注册函数
        if callback is None: callback = self.parse
        if callback.__name__ not in self._callback_priority_map.keys():
            self._callback_priority_map[callback.__name__] = self._next_priority_index
            self._next_priority_index += 1

        if priority is None: priority = self._callback_priority_map.get(callback.__name__)
        if not headers and hasattr(self, 'headers'): headers = self.headers
        if not cookies and hasattr(self, 'cookies'): cookies = self.cookies

        request_params = {
            'url': url,
            'method': method or 'GET',
            'data': data,
            'json': json,
            'headers': headers or {'User-Agent': random.choice(USER_AGENT_LIST)},
            'cookies': cookies,
            'allow_redirects': allow_redirects,
            **kwargs,
        }
        req = Request(**request_params)

        if self.filter is not None:
            if self.___fingerfilter(req, self.filter):
                return priority, req, callback, cb_args or (), cb_kwargs or {}
            else:
                self._count_map[-1] += 1
                self.logger.debug('Filter: {}'.format(req))
        else:
            return priority, req, callback, cb_args or (), cb_kwargs or {}

    def ___fingerfilter(self, request, filter):
        url = request.url
        args = [canonicalize_url(url)]

        for arg in ('data', 'files', 'auth', 'cert', 'json', 'cookies'):
            if request.__dict__.get(arg):
                args.append(request.__dict__.get(arg))

        finger = get_md5(*args)

        if isinstance(filter, set):
            if finger in filter:
                return False
            else:
                filter.add(finger)
                return True
        try:
            if isinstance(filter, Redis):
                if self.FILTER_TIMEOUT:
                    if self.filter.exists(self.FILTER_SKEY) and self.filter.ttl(self.FILTER_SKEY) == -1:
                        self.filter.expire(self.FILTER_SKEY, self.FILTER_TIMEOUT)

                if not self.filter.sadd(self.FILTER_SKEY, finger):
                    return False
                else:
                    return True
            else:
                self.logger.warning('Filter Type Warning: {}'.format(type(filter)))
                return True
        except Exception as e:
            self.logger.error('Filter Request Error: {}'.format(e))
            return True

    def prepare(self):
        pass

    def start_requests(self):
        yield ...

    def parse(self, response, *args, **kwargs):
        pass

    @staticmethod
    def __pipeline(item):
        if isinstance(item, dict):
            pprint(item)
        else:
            print(item)

    def close(self):
        pass
