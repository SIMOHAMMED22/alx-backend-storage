#!/usr/bin/env python3
"""task0"""

import redis
import uuid
from typing import Union, Callable, Optional, List
from functools import wraps


class Cache:
    def __init__(self):
        """
        Initialize the class instance by creating a Redis
                        connection and flushing the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


class Cache:
    def __init__(self):
        """
        Initializes a new instance of the class.

        :param self: The instance of the class.
        :return: None
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable =
            lambda x: x) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data)

    def get_str(self, key: str) -> str:
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        return self.get(key, int)


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()
        self.call_counts = {}

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable =
            lambda x: x) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data)

    def get_str(self, key: str) -> str:
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        return self.get(key, int)

    def count_calls(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            method_name = fn.__qualname__
            self.call_counts[method_name] = self.call_counts.get
            (method_name, 0) + 1
            return fn(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()
        self.call_counts = {}

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key:
            str, fn: Callable = lambda x: x) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data)

    def get_str(self, key: str) -> str:
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        return self.get(key, int)

    def count_calls(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            method_name = fn.__qualname__
            self.call_counts[method_name] = self.call_counts.get
            (method_name, 0) + 1
            return fn(self, *args, **kwargs)
        return wrapper

    def call_history(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = f"{method.__qualname__}:inputs"
            output_key = f"{method.__qualname__}:outputs"
            self._redis.rpush(input_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(output_key, str(output))
            return output
        return wrapper

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
