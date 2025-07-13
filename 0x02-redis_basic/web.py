#!/usr/bin/env python3
"""
Get page HTML and cache it in Redis with expiration.
Track access count per URL.
"""
import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()


def get_page(url: str) -> str:
    """
    Returns HTML content of a URL.
    Caches response for 10 seconds in Redis.
    Tracks how many times URL was accessed.
    """
    # Track number of accesses
    r.incr(f"count:{url}")

    # Check cache
    cached = r.get(f"cache:{url}")
    if cached:
        return cached.decode('utf-8')

    # Fetch from web and cache
    response = requests.get(url)
    content = response.text

    r.setex(f"cache:{url}", 10, content)
    return content
