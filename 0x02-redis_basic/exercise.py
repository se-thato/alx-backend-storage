#!/usr/bin/env python3
"""
Cache class using Redis to store data.
"""
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """
        Initialize Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis under a randomly generated key.
        Returns the key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key



"""
Cache class using Redis to store and retrieve data with optional formatting.
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """
        Initialize Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis under a randomly generated key.
        Returns the key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[bytes, str, int, float, None]:
        """
        Retrieve data from Redis using key.
        Optionally convert the data using a callable `fn`.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a UTF-8 string from Redis.
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.
        """
        return self.get(key, fn=int)
