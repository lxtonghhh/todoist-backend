# coding: utf-8
import logging
import threading
from contextlib import contextmanager
from functools import wraps, update_wrapper, lru_cache
import json
from .authentication import worker_login_authentication
from .exceptions import ResponseException
from .response_code import ResultCode
from .response import fail

logger = logging.getLogger(__name__)


def dummy_json(view_func):
    @wraps(view_func)
    def wrapper_view_func(request, *args, **kwargs):

        # Add simple validation or your own validation rule
        if request.content_type == 'application/json':
            if request.body:
                # Decode data to a dict object
                print('application/json')
                # print(str(request.body, encoding = "utf-8"))
                try:
                    request.json = json.loads(request.body)
                except:
                    raise ResponseException(ResultCode.POSTERR, "POST请求中Body格式错误，应该为json")

            else:
                raise ResponseException(ResultCode.POSTERR, "POST请求缺少Body")
        else:
            raise ResponseException(ResultCode.POSTERR, "请求内容类型错误,应该为:application/json")
        return view_func(request, *args, **kwargs)

    return wrapper_view_func


def _check_login_decorator(authentication):
    """
    :param session_key: 对应到Login之后，在session存的key是什么
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                authentication.authenticate(request)
                return func(request, *args, **kwargs)
            except ResponseException:
                return fail(sc=ResultCode.NOTLOGIN.value, msg="用户未登录")

        return wrapper

    return decorator


require_worker_login = _check_login_decorator(worker_login_authentication)


def try_catch(errors=(Exception,), handler=None, new_raise=None, new_return=None, log=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                if log:
                    logger.exception(e)
                if callable(handler):
                    handler(e)
                elif new_raise:
                    raise new_raise
                else:
                    return new_return

        return wrapper

    return decorator


@contextmanager
def ignore_exception(errors):
    try:
        yield
    except errors:
        pass


def singleton(cls):
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return wrapper


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


def factory(cls):
    @lru_cache(None)
    def get_instance(_cls, *args, **kwargs):
        return _cls(*args, **kwargs)

    @wraps(cls)
    def wrapper(*args, **kwargs):
        return get_instance(cls, *args, **kwargs)

    return wrapper


class memoize(object):
    """
    Memoize the result of a property call.

    >>> class A(object):
    >>>     @memoize
    >>>     def func(self):
    >>>         return 'foo'
    """

    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        """
        Call the function and put the return value in instance.__dict__ so that
        subsequent attribute access on the instance returns the cached value
        instead of calling cached_property.__get__().
        """
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res


def once(func):
    """Runs a thing once and once only."""
    lock = threading.Lock()

    def new_func(*args, **kwargs):
        if new_func.called:
            return
        with lock:
            if new_func.called:
                return
            rv = func(*args, **kwargs)
            new_func.called = True
            return rv

    new_func = update_wrapper(new_func, func)
    new_func.called = False
    return new_func
