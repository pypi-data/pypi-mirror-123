import logging
import os.path
import random
import asyncio
import re
import time
import aiohttp
from w3lib.url import canonicalize_url
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

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"
]


class Spider(object):

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

        self._next_priority_index = 0
        self._count = 0
        self._count_map = {-1: 0}
        self._callback_priority_map = {}
        self._start_time = time.time()

        self.LOG_LEVEL = logging.DEBUG
        self.LOG_FORMAT = '[%(log_color)s%(asctime)s%(reset)s] [%(log_color)s<%(name)s>%(levelname)8s%(reset)s] - %(log_color)s%(message)s%(reset)s'
        self.LOG_DATEFMT = '%Y/%m/%d %H:%M:%S'

        self.FILTER_TIMEOUT = 0
        self.FILTER_SKEY = self.name
        self.FILTER_DESTROY = True

        self.REQUEST_DELAY = 0
        self.REQUEST_FILTER = set()
        self.REQUEST_QUEUE = PriorityQueue()

        self.SPIDER_LOOP = asyncio.get_event_loop()
        self.SPIDER_DETAIL = False
        self.SPIDER_MAX_WORKER = 10
        self.SPIDER_STOP_COUNTDOWN = 3

        self.ITEM_PIPELINE = self.__pipeline
        self.USER_AGENT_LIST = USER_AGENT_LIST

        self.headers = None
        self.cookies = {}

        if os.path.exists('settings.py'):
            import settings as st
            for key in self.__dict__.keys() & st.__dict__.keys():
                self.__setattr__(key, st.__dict__.get(key))

            self.headers = {'User-Agent': random.choice(self.USER_AGENT_LIST)}

            if 'REQUEST_HEADERS' in st.__dict__.keys():
                self.headers = st.__dict__.get('REQUEST_HEADERS')

            if 'REQUEST_COOKIES' in st.__dict__.keys():
                self.cookies = st.__dict__.get('REQUEST_COOKIES')
        else:
            self.headers = {'User-Agent': random.choice(USER_AGENT_LIST)}

        self._sema = asyncio.Semaphore(self.SPIDER_MAX_WORKER)
        self.logger = logging.getLogger(self.name)

    def __init_logger(self):
        self.logger.setLevel(self.LOG_LEVEL)

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        formatter = ColoredFormatter(fmt=self.LOG_FORMAT, datefmt=self.LOG_DATEFMT)
        sh.setFormatter(formatter)

        self.logger.addHandler(sh)

    @property
    def max_worker(self):
        return self.SPIDER_MAX_WORKER

    @max_worker.setter
    def max_worker(self, num):
        self.SPIDER_MAX_WORKER = num
        self._sema = asyncio.Semaphore(num)

    def start(self):
        self.prepare()
        self.SPIDER_LOOP.run_until_complete(self.__run())
        self.close()

    async def __run(self):
        self.__init_logger()
        consumer = asyncio.ensure_future(self.__downloader())
        await self.__init_queue()
        await self.REQUEST_QUEUE.join()
        consumer.cancel()

        if self.REQUEST_FILTER is not None:
            try:
                if self.FILTER_DESTROY and isinstance(self.REQUEST_FILTER, Redis):
                    self.REQUEST_FILTER.delete(self.name)
                    self.logger.info('Delete Redis Filter Key: {}'.format(self.name))
            except NameError:
                pass
            except Exception as e:
                self.logger.error('Destroy Redis Filter Key Error: {}'.format(e))

    async def __init_queue(self):
        for item in self.start_requests():
            if item: await self.REQUEST_QUEUE.put(item)

    async def async_request(self, priority, req, callback, *args, **kwargs):

        if isinstance(req.__dict__.get('cookies', {}), str):
            req.__dict__['cookies'] = cookies_to_dict(req.__dict__.get('cookies'))

        if isinstance(req.__dict__.get('headers', {}), str):
            req.__dict__['headers'] = headers_to_dict(req.__dict__.get('cookies'))

        if self.REQUEST_DELAY: await asyncio.sleep(self.REQUEST_DELAY)

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

            if self.SPIDER_DETAIL or response.status_code != 200:
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
                        await self.REQUEST_QUEUE.put(req)
                    elif req and callable(self.ITEM_PIPELINE):
                        self.ITEM_PIPELINE(req)
            else:
                if result and callable(self.ITEM_PIPELINE):
                    self.ITEM_PIPELINE(result)

    async def __downloader(self):
        while self.SPIDER_STOP_COUNTDOWN >= 0:
            tasks = []
            for i in range(self.max_worker):
                if not self.REQUEST_QUEUE.empty():
                    with (await self._sema):
                        priority, req, callback, cb_args, cb_kwargs = await self.REQUEST_QUEUE.get()

                        task = self.SPIDER_LOOP.create_task(
                            self.async_request(
                                priority, req, callback, *cb_args, **cb_kwargs
                            )
                        )
                        tasks.append(task)
                else:
                    if not tasks:
                        self.SPIDER_STOP_COUNTDOWN -= 1
                    else:
                        await asyncio.gather(*tasks)
                        tasks.clear()

            if tasks:
                self.SPIDER_STOP_COUNTDOWN = 3
                await asyncio.gather(*tasks)

        if hasattr(self.REQUEST_QUEUE, '_finished'): self.REQUEST_QUEUE._finished.set()

    def request(self, url=None, method=None, data=None, json=None, headers=None, cookies=None, callback=None,
                cb_args=None, cb_kwargs=None, priority=None, allow_redirects=True, **kwargs):

        if callback is None: callback = self.parse
        if callback.__name__ not in self._callback_priority_map.keys():
            self._callback_priority_map[callback.__name__] = self._next_priority_index
            self._next_priority_index += 1

        if priority is None: priority = self._callback_priority_map.get(callback.__name__)
        if headers is None: headers = self.headers
        if cookies is None: cookies = self.cookies

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

        if self.REQUEST_FILTER is not None:
            if self.___fingerfilter(req, self.REQUEST_FILTER):
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
                    if self.REQUEST_FILTER.exists(self.FILTER_SKEY) and self.REQUEST_FILTER.ttl(self.FILTER_SKEY) == -1:
                        self.REQUEST_FILTER.expire(self.FILTER_SKEY, self.FILTER_TIMEOUT)

                if not self.REQUEST_FILTER.sadd(self.FILTER_SKEY, finger):
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
