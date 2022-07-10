#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    count how many times methods of the Cache class are called
    """
    @wraps(method)
    def inc(self, *args):
        """
        increments the count for that key
        every time the method is called
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args)
    return inc


def call_history(method: Callable) -> Callable:
    """
    store the history of inputs and outputs
    for a particular function
    """
    @wraps(method)
    def history(self, *args):
        """
        append the input arguments,
        and append the output too
        """
        inp_key = f'{method.__qualname__}:inputs'
        out_key = f'{method.__qualname__}:outputs'
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inp_key, str(args))
        stored = method(self, *args)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, stored)
        return stored
    return history


def replay(func):
    """
    function to display the history
    of calls of a particular function
    """
    redis_client = redis.Redis()
    if func is None or not isinstance(redis_client, redis.Redis):
        return
    func_count = 0
    inp_key = f'{func.__qualname__}:inputs'
    out_key = f'{func.__qualname__}:outputs'
    if redis_client.exists(func.__qualname__):
        func_count = int(redis_client.get(func.__qualname__))
    print(f'{func.__qualname__} was called {func_count} times:')
    inputs = redis_client.lrange(inp_key, 0, -1)
    outputs = redis_client.lrange(out_key, 0, -1)
    for inp, out in zip(inputs, outputs):
        print('{}(*{}) -> {}'.format(
                func.__qualname__,
                inp.decode("utf-8"),
                out.decode("utf-8")
        ))


class Cache:
    """Cache class"""
    def __init__(self) -> None:
        """init cache"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """write string data with random key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """Get Data from redis"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key):
        """get string value from redis"""
        return self.get(key, str)

    def get_int(self, key):
        """get int value from redis"""
        return self.get(key, int)
