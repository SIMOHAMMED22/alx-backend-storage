#!/usr/bin/env python3
"""exercise.py"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count calls"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """call history"""
    inputs = method.__qualname__ + ':inputs'
    outputs = method.__qualname__ + ':inputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """replay"""
    inputs = f'{method.__qualname__}:inputs'
    outputs = f'{method.__qualname__}:outputs'

    in_el = method.__self__._redis.lrange(inputs, 0, -1)
    out_el = method.__self__._redis.lrange(outputs, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(in_el)))
    for i, o in zip(in_el, out_el):
        print(
            f"{method.__qualname__}\
                (*{i.decode('utf-8')}) \
                    -> {o.decode('utf-8')}"
            )


class Cache:
    """cache class"""
    def __init__(self) -> None:
        """init"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key, fn=None) -> Union[str, bytes, int, float]:
        """get"""
        if fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))

    def get_str(self, key) -> str:
        """get_str"""
        return self.get(key, str)

    def get_int(self, key) -> int:
        """get_int"""
        return self.get(key, int)
