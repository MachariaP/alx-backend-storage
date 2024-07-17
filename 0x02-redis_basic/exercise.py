#!/usr/bin/env python3
"""
Defins a Cache class for interfacing with Redis, providing methods to store data
with unique keys and retrieve it, suitable for caching and temporary data storage.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Handles data storage and retrieval in Redis using unique keys.

    Attributes:
        _redis (redis.Redis): An instance of the Redis client.
    """


    def __init__(self):
        """
        Initializes Redis client and clears any existing data.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis under a unique key and returns the key.

        Args:
            data: Data to store. can be srt, bytes, int or float.

        Returns:
            The unique key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(name=key, value=data)
        return key
