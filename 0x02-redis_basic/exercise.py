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
