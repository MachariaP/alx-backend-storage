#!/usr/bin/env python3

import requests
import redis
from functools import wraps

r = redis.Redis()


def count_requests(func):
    """
    Decorator to count and cache requests.
    """
    @wraps(func)
    def wrapper(url):
        # Increment the count for the URL
        count_key = f"count:{url}"
        r.incr(count_key)

        # Check if the URL is already cached
        cached_content = r.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        # If not cached, call the original function
        # cache the result, and return it
        page_content = func(url)
        r.setex(url, 10, page_content)  # Cache with expiration of 10 seconds
        return page_content
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL, with caching and request counting.
    """
    response = requests.get(url)
    return response.text
