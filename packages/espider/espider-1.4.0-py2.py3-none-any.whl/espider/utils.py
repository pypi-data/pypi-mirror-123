import collections
import hashlib
import heapq
import random
import time
import warnings
from asyncio import events, locks
from functools import wraps
import json as Json
import re
from collections import defaultdict
from collections.abc import Iterable, Callable


class QueueEmpty(Exception):
    """Raised when Queue.get_nowait() is called on an empty Queue."""
    pass


class QueueFull(Exception):
    """Raised when the Queue.put_nowait() method is called on a full Queue."""
    pass


class PriorityQueue(object):
    """A queue, useful for coordinating producer and consumer coroutines.

    If maxsize is less than or equal to zero, the queue size is infinite. If it
    is an integer greater than 0, then "await put()" will block when the
    queue reaches maxsize, until an item is removed by get().

    Unlike the standard library Queue, you can reliably know this Queue's size
    with qsize(), since your single-threaded asyncio application won't be
    interrupted between calling qsize() and doing an operation on the Queue.
    """

    def __init__(self, maxsize=0, *, loop=None):
        if loop is None:
            self._loop = events.get_event_loop()
        else:
            self._loop = loop
            warnings.warn("The loop argument is deprecated since Python 3.8, "
                          "and scheduled for removal in Python 3.10.",
                          DeprecationWarning, stacklevel=2)
        self._maxsize = maxsize
        self.index = 0

        # Futures.
        self._getters = collections.deque()
        # Futures.
        self._putters = collections.deque()
        self._unfinished_tasks = 0
        self._finished = locks.Event(loop=loop)
        self._finished.set()
        self._init(maxsize)

    # These three are overridable in subclasses.

    def _init(self, maxsize):
        self._queue = []
        self._maxsize = maxsize or 0

    def _put(self, item):
        heapq.heappush(self._queue, (-item[0], self.index, item))
        self.index += 1

    def _get(self):
        if self._queue:
            return heapq.heappop(self._queue)[-1]

    # End of the overridable methods.

    def _wakeup_next(self, waiters):
        # Wake up the next waiter (if any) that isn't cancelled.
        while waiters:
            waiter = waiters.popleft()
            if not waiter.done():
                waiter.set_result(None)
                break

    def __repr__(self):
        return f'<{type(self).__name__} at {id(self):#x} {self._format()}>'

    def __str__(self):
        return f'<{type(self).__name__} {self._format()}>'

    def _format(self):
        result = f'maxsize={self._maxsize!r}'
        if getattr(self, '_queue', None):
            result += f' _queue={list(self._queue)!r}'
        if self._getters:
            result += f' _getters[{len(self._getters)}]'
        if self._putters:
            result += f' _putters[{len(self._putters)}]'
        if self._unfinished_tasks:
            result += f' tasks={self._unfinished_tasks}'
        return result

    def qsize(self):
        """Number of items in the queue."""
        return len(self._queue)

    @property
    def maxsize(self):
        """Number of items allowed in the queue."""
        return self._maxsize

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return not self._queue

    def full(self):
        """Return True if there are maxsize items in the queue.

        Note: if the Queue was initialized with maxsize=0 (the default),
        then full() is never True.
        """
        if self._maxsize <= 0:
            return False
        else:
            return self.qsize() >= self._maxsize

    async def put(self, item):
        """Put an item into the queue.

        Put an item into the queue. If the queue is full, wait until a free
        slot is available before adding item.
        """
        while self.full():
            putter = self._loop.create_future()
            self._putters.append(putter)
            try:
                await putter
            except:
                putter.cancel()  # Just in case putter is not done yet.
                try:
                    # Clean self._putters from canceled putters.
                    self._putters.remove(putter)
                except ValueError:
                    # The putter could be removed from self._putters by a
                    # previous get_nowait call.
                    pass
                if not self.full() and not putter.cancelled():
                    # We were woken up by get_nowait(), but can't take
                    # the call.  Wake up the next in line.
                    self._wakeup_next(self._putters)
                raise
        return self.put_nowait(item)

    def put_nowait(self, item):
        """Put an item into the queue without blocking.

        If no free slot is immediately available, raise QueueFull.
        """
        if self.full():
            raise QueueFull
        self._put(item)
        self._unfinished_tasks += 1
        self._finished.clear()
        self._wakeup_next(self._getters)

    async def get(self):
        """Remove and return an item from the queue.

        If queue is empty, wait until an item is available.
        """
        while self.empty():
            getter = self._loop.create_future()
            self._getters.append(getter)
            try:
                await getter
            except:
                getter.cancel()  # Just in case getter is not done yet.
                try:
                    # Clean self._getters from canceled getters.
                    self._getters.remove(getter)
                except ValueError:
                    # The getter could be removed from self._getters by a
                    # previous put_nowait call.
                    pass
                if not self.empty() and not getter.cancelled():
                    # We were woken up by put_nowait(), but can't take
                    # the call.  Wake up the next in line.
                    self._wakeup_next(self._getters)
                raise
        return self.get_nowait()

    def get_nowait(self):
        """Remove and return an item from the queue.

        Return an item if one is immediately available, else raise QueueEmpty.
        """
        item = self._get()
        self._wakeup_next(self._putters)
        return item

    def task_done(self):
        """Indicate that a formerly enqueued task is complete.

        Used by queue consumers. For each get() used to fetch a task,
        a subsequent call to task_done() tells the queue that the processing
        on the task is complete.

        If a join() is currently blocking, it will resume when all items have
        been processed (meaning that a task_done() call was received for every
        item that had been put() into the queue).

        Raises ValueError if called more times than there were items placed in
        the queue.
        """
        if self._unfinished_tasks <= 0:
            raise ValueError('task_done() called too many times')
        self._unfinished_tasks -= 1
        if self._unfinished_tasks == 0:
            self._finished.set()

    async def join(self):
        """Block until all items in the queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer calls task_done() to
        indicate that the item was retrieved and all work on it is complete.
        When the count of unfinished tasks drops to zero, join() unblocks.
        """
        if self._unfinished_tasks > 0:
            await self._finished.wait()


def fn_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Function [{}] Spend {:.3f} s".format(func.__name__, end - start))
        return result

    return wrapper


def _flatten(item):
    for k, v in item.items():
        if isinstance(v, dict):
            yield from _flatten(v)
        yield k, v


def json_to_dict(json):
    if isinstance(json, dict): return json

    if not json: return {}
    json = json.replace('\'', '"')
    try:
        return Json.loads(json)
    except:
        print(f'Invalid json data: {json}')
        return {}


def body_to_dict(data):
    if isinstance(data, dict): return data

    if not data: return {}
    assert '=' in data, f'Invalid data: {data}'
    return dict(_.split('=', 1) for _ in data.split('&'))


def _spilt_url(url):
    if not url: return {}
    path = url.split('?', 1)
    return [path[0], ''] if len(path) == 1 else path


def url_to_dict(url):
    if not url: return {}

    url = url.replace('://', '/')

    _path, _param = _spilt_url(url)
    protocol, domain, *path = _path.split('/')
    if _param:
        if '=' in _param:
            param = dict(p.split('=', 1) for p in _param.split('&'))
        else:
            param = {_param: _param}
    else:
        param = {}

    return {
        'protocol': protocol,
        'domain': domain,
        'path': path,
        'param': param
    }


def headers_to_dict(headers):
    if isinstance(headers, dict): return headers

    if not headers: return {}
    return {_.split(':', 1)[0].strip(): _.split(':', 1)[1].strip() for _ in headers.split('\n') if
            len(_.split(':', 1)) == 2}


def cookies_to_dict(cookies):
    if isinstance(cookies, dict): return cookies

    if not cookies: return {}
    return {_.split('=', 1)[0].strip(): _.split('=', 1)[1].strip() for _ in cookies.strip('\n;').split(';')}


def dict_to_body(data: dict):
    return '&'.join([f'{key}={value}' for key, value in data.items()])


def dict_to_json(json: dict):
    return Json.dumps(json)


def search(key, data=None, target_type=None):
    my_dict = defaultdict(list)
    for k, v in _flatten(data):
        my_dict[k].append(v)

    if isinstance(key, Iterable) and not isinstance(key, (str, bytes)):
        return {
            k: [_ for _ in my_dict.get(k) if isinstance(_, target_type)] if target_type else my_dict.get(k)
            for k in key
        }
    else:
        result = [_ for _ in my_dict.get(key) if isinstance(_, target_type)] if target_type else my_dict.get(key)
        return result[0] if result and len(result) == 1 else result


def strip(*args, data=None, strip_key=False):
    if not data: args, data = args[:-1], args[-1]

    for st_key in args:
        if isinstance(st_key, (str, Callable)): st_key = [st_key]

        for r in st_key:
            result = {}
            for key, value in data.items():
                key, value = _strip(key, value, r, strip_key=strip_key)
                result[key] = value
            data = result

    return data


def replace(replace_map=None, data=None, replace_key=False):
    assert isinstance(data, dict), 'item must be dict'

    for r_key, r_value in replace_map.items():
        result = {}
        for key, value in data.items():
            key = key if not replace_key else key.replace(r_key, r_value)
            if isinstance(value, str):
                result[key] = value.replace(r_key, r_value)
            elif isinstance(value, dict):
                result[key] = replace(data=value, replace_key=replace_key, replace_map={r_key: r_value})
            elif isinstance(value, list):
                result[key] = _process_list(key, value, rule=(r_key, r_value), process_key=replace_key)
            else:
                result[key] = value
        data = result

    return data


def update(update_map, data=None, target_type=None):
    assert isinstance(data, dict), 'item must be dict'
    if not target_type: target_type = (str, bytes, int, float, list, dict)

    for u_key, u_value in update_map.items():
        result = {}
        for key, value in data.items():
            if isinstance(value, target_type) and not isinstance(value, dict):
                result[key] = u_value if key == u_key else value
            elif isinstance(value, dict):
                result[key] = update(update_map={u_key: u_value}, data=value, target_type=target_type)
            else:
                result[key] = value
        data = result

    return data


def delete(*args, data=None, target_type=None):
    if not data: args, data = args[:-1], args[-1]
    if not target_type: target_type = (str, bytes, int, float, list, dict)

    for d_key in args:
        assert isinstance(d_key, (str, list, tuple)), f'args must be str、list or tuple, get {d_key}'

        if isinstance(d_key, str): d_key = [d_key]
        for d_k in d_key:
            result = {}
            for key, value in data.items():
                if isinstance(value, target_type):
                    if key == d_k:
                        continue
                    else:
                        result[key] = value
                elif isinstance(value, dict):
                    result[key] = delete(d_k, data=value, target_type=target_type)
                else:
                    result[key] = value
            data = result

    return data


def _strip(key, value, rule, strip_key=False):
    if type(rule).__name__ == 'function':
        rule, switch = rule(key, value)
        if not switch: return key, value

    key = key.replace(rule, '') if strip_key else key

    if isinstance(value, (str, int, float)):
        value = value if not isinstance(value, str) else value.replace(rule, '')
    elif isinstance(value, dict):
        value = strip(rule, data=value, strip_key=strip_key)
    elif isinstance(value, list):
        value = _process_list(key, value, rule, process_key=strip_key)

    return key, value


def _process_list(key, value, rule, process_key=False):
    s = False
    if isinstance(rule, str): rule, s = (rule, ''), True

    result = []
    for v in value:
        if isinstance(v, str):
            result.append(v.replace(*rule))
        elif isinstance(v, list):
            if s:
                v = _strip(key, v, rule[0], strip_key=process_key)
            else:
                v = replace(replace_key=process_key, data={'_': v}, replace_map={rule[0]: rule[1]})

            result.append(v)
        elif isinstance(v, dict):
            if s:
                v = strip(rule, data=v, strip_key=process_key)
            else:
                v = replace(replace_key=process_key, data=v, replace_map={rule[0]: rule[1]})
            result.append(v)
        else:
            result.append(v)

    return result


def flatten(data):
    for k, v in data.items():
        if isinstance(v, dict):
            yield from flatten(v)
        else:
            yield k, v


def re_search(re_map, data, flags=None, index=None):
    s = False
    if isinstance(re_map, str): re_map, s = {'_': re_map}, True
    result = {}
    for key, pattern in re_map.items():
        if isinstance(pattern, str):
            r = re.search(pattern, data, flags=flags or 0)
            if not r and not flags:
                r = re.search(pattern, data, flags=re.S)
        elif isinstance(pattern, re.Pattern):
            r = pattern.search(data)
        elif isinstance(pattern, dict):
            r = re_search(pattern, data, flags=flags, index=index)
        else:
            raise Exception(f'Type Error ... re_search not support {type(pattern)}')

        result[key] = r

    result_g = _get_group_data(result, index=index)

    return result_g if not s else result_g.get('_')


def _get_group_data(data, index=None):
    result_g = {}
    for k, v in data.items():
        if v and isinstance(v, dict):
            result_g[k] = _get_group_data(v)
        elif isinstance(v, str):
            result_g[k] = v
        else:
            try:
                result_g[k] = v.group(index or 0) if v else ''
            except IndexError:
                result_g[k] = v.group()

    return result_g


def re_findall(re_map, data, flags=None, iter=False):
    s = False
    if isinstance(re_map, str): re_map, s = {'_': re_map}, True

    result = {}
    for key, pattern in re_map.items():
        if isinstance(pattern, str):
            r = re.finditer(pattern, data, flags=flags or 0) if iter else re.findall(pattern, data, flags=flags or 0)
            if not r and not flags:
                r = re.search(pattern, data, flags=re.S)
        elif isinstance(pattern, re.Pattern):
            r = pattern.finditer(data) if iter else pattern.findall(data)
        elif isinstance(pattern, dict):
            r = re_findall(pattern, data, flags=flags, iter=iter)
        else:
            raise Exception(f'Type Error ... re_search not support {type(pattern)}')

        result[key] = r

    return result if not s else result.get('_')


def merge(*args, overwrite=False):
    default_dict = defaultdict(list)

    v_dict = defaultdict(list)
    for d in args:
        if not isinstance(d, dict): continue
        for k, v in d.items():
            if isinstance(v, dict):
                v_dict[k].append(v)
                continue
            if overwrite and default_dict.get(k) and v in default_dict.get(k): continue
            default_dict[k].append(v)

    for k, v in v_dict.items():
        default_dict[k].append(merge(*v, overwrite=overwrite))

    return {k: v[0] if k in v_dict.keys() else v for k, v in dict(default_dict).items()}


def args_split(args: tuple):
    arg = tuple(i for i in args if not isinstance(i, dict))
    kwarg = [i for i in args if isinstance(i, dict)]

    if len(kwarg) >= 1:
        _kwargs = {}
        for i in kwarg:
            _kwargs.update(i)
        kwarg = _kwargs

    return arg, kwarg or {}


def random_list(stop, start=0, step=1):
    numbers = list(range(start, stop + start, step))
    random.shuffle(numbers)
    return numbers


def human_time(time_stamp):
    days = time_stamp // 86400
    hours = (time_stamp % 86400) // 3600
    minutes = (time_stamp % 3600) // 60
    seconds = (time_stamp % 60)
    return days, hours, minutes, seconds


def get_md5(*args):
    """
    @summary: 获取唯一的32位md5
    ---------
    @param *args: 参与联合去重的值
    ---------
    @result: 7c8684bcbdfcea6697650aa53d7b1405
    """

    m = hashlib.md5()
    for arg in args:
        m.update(str(arg).encode())

    return m.hexdigest()
