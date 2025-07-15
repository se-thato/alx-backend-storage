#!/usr/bin/env python3
"""
Module to cache a web page and track access count using Redis
"""
import redis
import requests

_redis = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL.
    Caches the result with a 10-second expiration.
    Tracks how many times the URL has been accessed.
    """
    cache_key = url
    count_key = f"count:{url}"

    # Increment count (used for scoring)
    _redis.incr(count_key)

    # Return cached value if it exists
    cached = _redis.get(cache_key)
    if cached:
        return cached.decode('utf-8')

    # Otherwise fetch from web
    response = requests.get(url)
    content = response.text

    # Cache it with 10-second TTL
    _redis.setex(cache_key, 10, content)
    return content

