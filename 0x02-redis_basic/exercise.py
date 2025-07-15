#!/usr/bin/env python3
"""
Module for Cache class with Redis integration and decorators for call counting,
history tracking, and replay functionality.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.

    Args:
        method (Callable): The method to wrap.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increment call count in Redis and call the original method."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method.

    Args:
        method (Callable): The method to wrap.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Store input args and output results in Redis lists."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The method whose history will be displayed.
    """
    redis_instance = method.__self__._redis
    qualname = method.__qualname__

    inputs = redis_instance.lrange(f"{qualname}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{qualname}:outputs", 0, -1)

    print(f"{qualname} was called {len(inputs)} times:")

    for input_val, output_val in zip(inputs, outputs):
        print(f"{qualname}(*{input_val.decode('utf-8')}) -> "
              f"{output_val.decode('utf-8')}")


class Cache:
    """
    Cache class to interact with Redis for storing data with unique keys.

    Provides methods to store data, retrieve it with optional
    conversion functions, and tracks method calls and their history.
    """

    def __init__(self):
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The generated Redis key where data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float,
                                                   None]:
        """
        Retrieve data from Redis and optionally convert it.

        Args:
            key (str): The Redis key to retrieve.
            fn (Optional[Callable], optional): A function to convert
                the data. Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data,
            possibly converted, or None if key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data as a UTF-8 decoded string.

        Args:
            key (str): The Redis key.

        Returns:
            Optional[str]: The decoded string or None.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data as an integer.

        Args:
            key (str): The Redis key.

        Returns:
            Optional[int]: The integer value or None.
        """
        return self.get(key, fn=int)
