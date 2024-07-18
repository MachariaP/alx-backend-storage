#!/usr/bin/env python3
"""Implement a get_page function to fetch HTML content of URLs with caching.

This script defines a `get_page` function that fetches the HTML content of a
given URL using the requests module. It enhances performance and efficiency by
caching the results of these requests for a short duration and tracking the
number of times each URL is accessed.

Features:
- Fetch HTML content of URLs.
- Cache results to reduce repeated requests.
- Count and track the number of accesses for each URL.

Usage:
To use this functionality, ensure a Redis server is running and accessible.
Then, call the `get_page` function with the desired URL. For testing purposes,
you can use http://slowwly.robertomurray.co.uk to simulate a slow response.

Example:
    get_page('http://example.com')

Note:
Start with a new file named web.py and avoid reusing code from
previous exercises.
"""

import redis
import requests
from functools import wraps

r = redis.Redis()


def url_access_count(method):
    """Decorator to enhance get_page with caching and access counting."""
    @wraps(method)
    def wrapper(url):
        """Cache results and count URL accesses."""
        # Increment the count each time a URL is accessed
        key_count = "count:" + url
        current_count = r.incr(key_count)

        # Check if the URL is already cached
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            # If cached, return the cached value
            return cached_value.decode("utf-8")
        else:
            # If not cached, fetch the content and cache it
            html_content = method(url)
            r.set(key, html_content, ex=10)
            return html_content
        return wrapper


@url_access_count
def get_page(url: str) -> str:
    """Fetch and return the HTML content of a specified URL."""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
