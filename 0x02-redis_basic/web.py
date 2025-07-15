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

    # Increment access count
    _redis.incr(count_key)

    # Return cached content if available
    cached = _redis.get(cache_key)
    if cached:
        return cached.decode('utf-8')

    # Fetch content from web
    response = requests.get(url)
    content = response.text

    # Cache the content for 10 seconds
    _redis.setex(cache_key, 10, content)

    return content

