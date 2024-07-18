#!/usr/bin/env python3
"""
Defins a Cache class for interfacing with Redis, providing methods to store data
with unique keys and retrieve it, suitable for caching and temporary data storage.
"""

import redis
import uuid
import functools
from typing import Union, Optional, Callable

def call_history(method: Callable) -> Callable:
    """
    A decorator to store the history of inputs for a particular func.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Normalize and store input arguments
        inputs_key = f"{method.__qualname__}:inputs"
        self._redis.rpush(inputs_key, str(args))

        # Execute the wrapped function and store its output
        output = method(self, *args, **kwargs)
        outputs_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(outputs_key, str(output))

        return output
    return wrapper


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

    @call_history
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


    def get(self, key: str, fn: Optional[callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis by key and converts it using the provided function.

        Args:
            key: The key of the data to retrieve.
            fn: An optional callable to convert the data back to its desired format.

        Returns:
            The retrieved data, optionally converted using fn or None if key doesn't exist.
        """
        value = self._redis.get(name=key)
        if value is not None and fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves a string from Redis.

        Args:
            key: The key of the data to retrieve.

        Returns:
            The retrieved string or None if the key doesn't exist.
        """
        value = self.get(key, fn=lambda x: x.decode('utf-8') if x else None)
        return value

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves an integer from Redis.

        Args:
            key: The key of the data to retrieve.

        Returns:
            The retrieved integer or None if key doesn't exist.
        """
        return self.get(key, fn=int)
