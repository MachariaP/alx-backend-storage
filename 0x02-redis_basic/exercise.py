#!/usr/bin/env python3
"""
Defins a Cache class for interfacing with Redis, providing methods
to store data with unique keys and retrieve it, suitable for
caching and temporary data storage.
"""

import redis
import uuid
import functools
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """
    A decorator to store the history of inputs for a particular func.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Normalize and store input arguments
        """
        key = f"count:{method.__qualname__}"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Handles data storage and retrieval in Redis using unique keys.

    Attributes:
        _redis (redis.Redis): An instance of the Redis client.
    """

    def __init__(self, host='localhost', port=6379, db=0):
        """
        Initializes Redis client and clears any existing data.
        """
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis under a unique key and returns the key.

        Args:
            data: Data to store. can be srt, bytes, int or float.

        Returns:
            The unique key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[callable] = None
            ) -> Union[str, bytes, int, float]:
        """
        Retrieves data from Redis by key and
        converts it using the provided function.

        Args:
            key: The key of the data to retrieve.
            fn: An optional callable to convert the data back to
            its desired format.

        Returns:
            The retrieved data, optionally converted using fn or None
            if key doesn't exist.
        """
        data = self._redis.get(key)
        if data is None:
            return data
        if fn:
            callable_fn = fn(data)
            return callable_fn
        else:
            return data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string from Redis.

        Args:
            key: The key of the data to retrieve.

        Returns:
            The retrieved string or None if the key doesn't exist.
        """
        value = self._redis.get(key, fn=lambda x: x.decode('utf-8'))
        return value

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer from Redis.

        Args:
            key: The key of the data to retrieve.

        Returns:
            The retrieved integer or None if key doesn't exist.
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            return None

        return value

    def replay(method: Callable):
        """
        Display the history of calls of a particular function.
        """
        instance = method.__self__   # Get the instance (Cache) for the method
        method_name = method.__qualname__
        inputs_key = f"{method_name}:inputs"
        outputs_key = f"{method_name}:outputs"

        inputs = instance._redis.lrange(inputs_key, 0, -1)
        outputs = instance._redis.lrange(outputs_key, 0, -1)

        print(f"{method_name} was called {len(inputs)} times:")
        for input_str, output_str in zip(inputs, outputs):
            input_decode = input_str.decode('utf-8')
            output_decode = output_str.decode('utf-8')
            print(f"{method_name} {input_decode} -> {output_decoded}")
