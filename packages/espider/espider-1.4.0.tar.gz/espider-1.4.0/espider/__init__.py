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
from pprint import pformat
from espider._utils._colorlog import ColoredFormatter
from collections.abc import Iterable, Coroutine

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

        self._msg_total_requests = 0
        self._msg_runtime = 0
        self._msg_items = 0
        self._msg_item_speed = 0
        self._msg_item_dropped = 0
        self._msg_download_speed = 0
        self._msg_request_dropped = 0
        self._msg_response_dropped = 0

        self._priority_item_map = {}
        self._priority_request_map = {}
        self._priority_callback_map = {}
        self._next_priority_index = 1

        self._default_filter_queue = set()
        self._response_filter_code = [404]

        self.LOG_LEVEL = logging.DEBUG
        self.LOG_FORMAT = '[%(log_color)s%(asctime)s%(reset)s] [%(log_color)s<%(name)s>%(levelname)8s%(reset)s] - %(log_color)s%(message)s%(reset)s'
        self.LOG_DATEFMT = '%Y/%m/%d %H:%M:%S'

        self.REQUEST_DELAY = 0
        self.REQUEST_WARNING = True
        self.REQUEST_QUEUE = PriorityQueue()
        self.REQUEST_MIDDLEWARES = [self.__request_filter]
        self.REQUEST_BATCH_SIZE = 10
        self.REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=600)
        self.REQUEST_CONNECTOR = aiohttp.TCPConnector(limit=100)
        self.REQUEST_SESSION = aiohttp.ClientSession(connector=self.REQUEST_CONNECTOR, timeout=self.REQUEST_TIMEOUT)

        self.SPIDER_LOOP = asyncio.get_event_loop()
        self.SPIDER_STOP_COUNTDOWN = 3

        self.ITEM_PIPELINES = [self.__pipeline]
        self.USER_AGENT_LIST = USER_AGENT_LIST
        self.RESPONSE_MIDDLEWARES = [self.__response_filter]

        self.headers = self.headers if hasattr(self, 'headers') else None
        self.cookies = self.cookies if hasattr(self, 'cookies') else {}

        if os.path.exists('settings.py'):
            import settings as st
            for key in self.__dict__.keys() & st.__dict__.keys():
                self.__setattr__(key, st.__dict__.get(key))

            if 'REQUEST_HEADERS' in st.__dict__.keys():
                self.headers = st.__dict__.get('REQUEST_HEADERS')

            if 'REQUEST_COOKIES' in st.__dict__.keys():
                self.cookies = st.__dict__.get('REQUEST_COOKIES')

        self.logger = logging.getLogger(self.name)
        self._start_time = time.time()

    def start(self):
        self.prepare()
        self.SPIDER_LOOP.run_until_complete(self.__run())
        self.close()

    @property
    def msg(self):
        return {
            'items': self._msg_items,
            'requests': self._msg_total_requests,
            'runtime': round(self._msg_runtime, 2),
            'item_speed': round(self._msg_item_speed, 2),
            'download_speed': round(self._msg_download_speed, 2),
            'item_dropped': self._msg_item_dropped,
            'request_dropped': self._msg_request_dropped,
            'response_dropped': self._msg_response_dropped,
        }

    def __assert_params(self):

        if callable(self.ITEM_PIPELINES):
            self.ITEM_PIPELINES = [self.ITEM_PIPELINES]

        assert isinstance(self.ITEM_PIPELINES, Iterable), \
            'ITEM_PIPELINE type error: except function or function list, get {}.'.format(self.ITEM_PIPELINES)

        for pipe in self.ITEM_PIPELINES:
            assert callable(pipe), 'ITEM_PIPELINE({}) not callable'.format(pipe)

        if self.REQUEST_MIDDLEWARES is not None:
            if callable(self.REQUEST_MIDDLEWARES):
                self.REQUEST_MIDDLEWARES = [self.REQUEST_MIDDLEWARES]
            self.__check_middlewares(self.REQUEST_MIDDLEWARES)

        if self.RESPONSE_MIDDLEWARES is not None:
            if callable(self.RESPONSE_MIDDLEWARES):
                self.RESPONSE_MIDDLEWARES = [self.RESPONSE_MIDDLEWARES]
            self.__check_middlewares(self.RESPONSE_MIDDLEWARES)

    @staticmethod
    def __check_middlewares(middlewares):
        assert isinstance(middlewares, Iterable), \
            'MIDDLEWARES type error: except function or function list, get {}.'.format(middlewares)
        for mid in middlewares:
            assert callable(mid), 'Middleware {} not callable.'.format(mid)

    def __init_logger(self):
        self.logger.setLevel(self.LOG_LEVEL)
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        formatter = ColoredFormatter(fmt=self.LOG_FORMAT, datefmt=self.LOG_DATEFMT)
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

    async def __init_queue(self):
        for r in self.start_requests():
            if not r: continue
            if isinstance(r, tuple) and isinstance(r[1], Request):
                await self.REQUEST_QUEUE.put(r)
            else:
                await self.__process_item(1, r)

    async def __run(self):
        """
        主函数
        """
        try:
            self.__assert_params()
            self.__init_logger()
        except Exception as e:
            self.logger.exception(e)
        else:
            consumer = asyncio.ensure_future(self.__downloader())
            await self.__init_queue()
            await self.REQUEST_QUEUE.join()
            await self.REQUEST_SESSION.close()
            consumer.cancel()

    def request(self, url=None, method=None, data=None, json=None, headers=None, cookies=None, callback=None,
                cb_args=None, cb_kwargs=None, priority=None, allow_redirects=True, **kwargs):
        """
        请求创建函数
        """

        if callback is None: callback = self.parse
        if callback.__name__ not in self._priority_callback_map.keys():
            self._priority_callback_map[callback.__name__] = self._next_priority_index
            self._next_priority_index += 1

        if priority is None: priority = self._priority_callback_map.get(callback.__name__)

        request_params = {
            'url': url,
            'method': method or 'GET',
            'data': data,
            'json': json,
            'headers': headers,
            'cookies': cookies,
            'allow_redirects': allow_redirects,
            **kwargs,
        }
        return priority, Request(**request_params), callback, cb_args or (), cb_kwargs or {}

    async def async_request(self, priority, req, callback, *args, **kwargs):
        """
        异步请求
        """
        try:
            # 处理请求
            req = await self.__process_request(req)
            if req is None: return

            if self.REQUEST_DELAY: await asyncio.sleep(self.REQUEST_DELAY)

            msg = self.__collect_msg(priority, req)
            self.logger.info(msg)
            # FIXME aiohttp.client_exceptions.ServerDisconnectedError
            async with self.REQUEST_SESSION.request(**req.__dict__) as _resp:
                data = await _resp.read()
                resp = Response(_resp)
                resp.text = data
                resp.request = req
                if self.REQUEST_WARNING and resp.status_code != 200:
                    detail = pformat(req.__dict__).replace('\n', '\n\t\t')
                    detail = re.sub('^\{', '{\n\t\t ', detail)
                    detail = re.sub('\}$', '\n\t}', detail)
                    msg = msg + '{}\n\t{}\n'.format(resp.status_code, detail)
                    self.logger.warning(msg)

            # 更新爬虫信息
            self.__update_msg(priority)

            # 处理响应
            resp = await self.__process_response(resp)
            if resp is None: return

        except Exception as e:
            self.logger.exception(msg=f"Async Request Error: {e}")
        else:
            # 处理回调函数
            await self.__process_callback(priority, callback, resp, *args, **kwargs)

    async def __process_request(self, req):

        if not req.headers: req.headers = self.headers or {'User-Agent': random.choice(self.USER_AGENT_LIST)}
        if isinstance(req.headers, str): req.headers = headers_to_dict(req.headers)
        if not req.cookies: req.cookies = self.cookies
        if isinstance(req.cookies, str): req.cookies = cookies_to_dict(req.cookies)
        # 调用请求中间件
        req = await self.__process_middleware(req, self.REQUEST_MIDDLEWARES)
        if req is None:
            self._msg_request_dropped += 1
            return
        return req

    async def __process_response(self, resp):
        # 调用响应中间件
        resp = await self.__process_middleware(resp, self.RESPONSE_MIDDLEWARES)
        if resp is None:
            self._msg_response_dropped += 1
            return
        return resp

    @staticmethod
    async def __process_middleware(req, middlewares):
        if not middlewares: return req
        for mid in middlewares:
            req = mid(req)
            if isinstance(req, Coroutine): req = await req
            if not req: return
        return req

    async def __process_callback(self, priority, callback, resp, *args, **kwargs):
        """
        处理回调函数
        """
        try:
            result = callback(resp, *args, **kwargs)
            if isinstance(result, Coroutine): result = await result
        except Exception as e:
            self.logger.exception(msg='Process Callback({}) Error: {}'.format(callback.__name__, e))
        else:
            if not result: return
            if isgenerator(result):
                for r in result:
                    if not r: continue
                    if isinstance(r, tuple) and isinstance(r[1], Request):
                        self.REQUEST_QUEUE.put_nowait(r)
                    else:
                        await self.__process_item(priority, r)
            else:
                await self.__process_item(priority, result)

    async def __downloader(self):
        """
        请求调度函数
        """
        while self.SPIDER_STOP_COUNTDOWN >= 0:
            tasks = []
            if self.REQUEST_BATCH_SIZE != 0:
                if not self.REQUEST_QUEUE.empty():
                    for _ in range(self.REQUEST_BATCH_SIZE):
                        param = self.REQUEST_QUEUE.get_nowait()
                        if not param: continue
                        task = self.__create_task(param)
                        tasks.append(task)

                    await asyncio.gather(*tasks)
                    self.SPIDER_STOP_COUNTDOWN = 3
                else:
                    self.SPIDER_STOP_COUNTDOWN -= 1
                    if self.SPIDER_STOP_COUNTDOWN < 0:
                        self.__close_msg()
            else:
                if self.REQUEST_QUEUE.empty():
                    self.SPIDER_STOP_COUNTDOWN -= 1
                else:
                    self.SPIDER_STOP_COUNTDOWN = 3
                while not self.REQUEST_QUEUE.empty():
                    task = self.__create_task(self.REQUEST_QUEUE.get_nowait())
                    tasks.append(task)
                await asyncio.gather(*tasks)

        if hasattr(self.REQUEST_QUEUE, '_finished'):
            self.REQUEST_QUEUE._finished.set()

    async def __create_task(self, task_params):
        priority, req, callback, cb_args, cb_kwargs = task_params
        return await self.SPIDER_LOOP.create_task(
            self.async_request(
                priority, req, callback, *cb_args, **cb_kwargs
            )
        )

    async def __process_item(self, priority, item):
        """
        处理数据管道
        """
        try:
            for pipe in self.ITEM_PIPELINES:
                item = pipe(item)
                if isinstance(item, Coroutine): item = await item
                if item is None:
                    self._msg_item_dropped += 1
        except Exception as e:
            self.logger.exception(e)
        else:
            # 更新 Item 信息
            self._msg_items += 1
            self._msg_item_speed = self._msg_items / (self._msg_runtime or 1)
            if str(priority) not in self._priority_item_map.keys(): self._priority_item_map[str(priority)] = 0
            self._priority_item_map[str(priority)] += 1

    def __update_msg(self, priority):
        self._msg_runtime = time.time() - self._start_time
        self._msg_total_requests += 1
        self._msg_download_speed = self._msg_total_requests / (self._msg_runtime or 1)

        if str(priority) not in self._priority_request_map.keys(): self._priority_request_map[str(priority)] = 0
        self._priority_request_map[str(priority)] += 1

    @staticmethod
    def __split_result(result):
        if isinstance(result, (dict, list, str)):
            return result, 1

        if isinstance(result, tuple):
            if len(result) == 1:
                return result[0], 1
            else:
                if isinstance(result[-1], dict):
                    item, *args, kwargs = result
                    return item, args, kwargs, 3
                else:
                    item, *args = result
                    return item, args, 2
        else:
            return result, 1

    async def __request_filter(self, req):
        url = req.url
        args = [canonicalize_url(url)]

        for arg in ('data', 'files', 'auth', 'cert', 'json', 'cookies'):
            if req.__dict__.get(arg):
                args.append(req.__dict__.get(arg))

        finger = get_md5(*args)

        if finger not in self._default_filter_queue:
            self._default_filter_queue.add(finger)
            return req
        else:
            self.logger.warning("Drop {}".format(req))

    def __response_filter(self, resp):
        if resp.status_code in self._response_filter_code:
            self.logger.warning("Drop {}".format(resp))
        return resp

    def prepare(self):
        pass

    def start_requests(self):
        yield ...

    def parse(self, response, *args, **kwargs):
        pass

    def __pipeline(self, item):
        self.logger.debug('Item: {}'.format(item))
        return item

    def close(self):
        pass

    def __collect_msg(self, priority, req):

        return '[{}] [{:.2f}] [{}/{:.2f}] [{}/{:.2f}] {} {}'.format(
            priority,
            self._msg_runtime,
            self._msg_total_requests,
            self._msg_download_speed,
            self._msg_items,
            self._msg_item_speed,
            req.__dict__.get('method'),
            req.__dict__.get('url'),
        )

    def __close_msg(self):
        self.logger.info('-' * 100)
        self.logger.info('Spider - {:21s}: {}'.format(
            'Dropped', {k: v for k, v in self.msg.items() if 'dropped' in k}
        ))
        self.logger.info('Spider - {:21s}: {}'.format(
            'Speed', {k: v for k, v in self.msg.items() if 'speed' in k}
        ))
        self.logger.info('Spider - {:21s}: {}'.format(
            'Download', {k: v for k, v in self.msg.items() if 'speed' not in k and 'dropped' not in k}
        ))
        self.logger.info('Spider - {:21s}: {}'.format(
            'Priority Item',
            self._priority_item_map,
        ))
        self.logger.info('Spider - {:21s}: {}'.format(
            'Priority Request',
            self._priority_request_map,
        ))
        self.logger.info('Spider - {:21s}: {}'.format(
            'Item Pipelines', [m.__name__ for m in self.ITEM_PIPELINES]
        ))
        self.logger.info('Spider - {:21s}: {}'.format(
            'Request Middlewares', [m.__name__ for m in self.REQUEST_MIDDLEWARES]
        ))
        self.logger.info('Spider - {:21s}: {}'.format(
            'Response Middlewares', [m.__name__ for m in self.RESPONSE_MIDDLEWARES]
        ))
        self.logger.info('-' * 100)
