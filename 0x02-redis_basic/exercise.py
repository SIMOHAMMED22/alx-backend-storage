#!/usr/bin/env python3
"""Main"""

import redis
import uuid
from typing import Union, Callable, Optional, List
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count how many times methods of Cache class are called"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap the decorated"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ store the history  """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapped function """
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper

    def replay(method: Callable):
        """
        Display the history of calls of a particular function
        """
        inputs = method.__qualname__ + ":inputs"
        outputs = method.__qualname__ + ":outputs"
        count = method.__self__._redis.llen(inputs)
        print(f"{method.__qualname__} was called {count} times:")
        for inp, out in zip(method.__self__._redis.lrange(inputs, 0, -1),
                            method.__self__._redis.lrange(outputs, 0, -1)):
            print(f"{method.__qualname__}{inp.decode(
                'utf-8')} -> {out.decode('utf-8')}")


class Cache:
    """ class """

    def __init__(self):
        """ init redis """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ generate a random key to store data """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ convert data using cb """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ automatically parametrize Cache.get to str """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ automatically parametrize Cache.get to int """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
