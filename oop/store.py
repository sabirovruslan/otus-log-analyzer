from abc import ABCMeta
from functools import wraps
from time import sleep

from pymemcache.client.base import Client


def retrying(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        attempts = 1
        while True:
            try:
                return f(self, *args, **kwargs)
            except Exception as e:
                if attempts == self._reconnect_attempts:
                    raise
                attempts += 1
                sleep(self._reconnect_timeout)

    return decorator


class CacheAdapter:
    __metaclass__ = ABCMeta

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, time=0):
        raise NotImplementedError


class MemcacheAdapter(CacheAdapter):
    DEFAULT_TIMEOUT = 10

    def __init__(self, **kwargs):
        self.client = Client(
            server=(kwargs.get('address'), int(kwargs.get('port'))),
            connect_timeout=kwargs.get('connect_timeout', self.DEFAULT_TIMEOUT),
            timeout=kwargs.get('timeout', self.DEFAULT_TIMEOUT),
            ignore_exc=kwargs.get('ignore_exc', True)
        )

    def get(self, key):
        result = self.client.get(key)
        return result.decode('utf-8') if isinstance(result, bytes) else result

    def set(self, key, value, time=0):
        self.client.set(key, value, expire=time)


class Store:

    def __init__(self, cache_adapter: CacheAdapter, reconnect_attempts=1, reconnect_timeout=0):
        self._cache = cache_adapter
        self._reconnect_attempts = reconnect_attempts
        self._reconnect_timeout = reconnect_timeout

    def get(self, key):
        return self._cache.get(key)

    @retrying
    def cache_get(self, key):
        return self._cache.get(key)

    @retrying
    def cache_set(self, key, value, time=0):
        return self._cache.set(key, value, time)