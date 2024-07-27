#!/usr/bin/env python3
import redis
import uuid
import functools
from typing import Union, Optional, Callable, Any


def count_calls(method: Callable) -> Callable:
    """Count the number of calls to the decorated method."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        key = f"count:{method.__qualname__}"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a function."""
    def wrapper(self, *args, **kwargs):
        input_str = str(args)
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, input_str)
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


class Cache:
    """Handles data storage and retrieval in Redis."""
    def __init__(self, host='localhost', port=6379, db=0):
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis under a unique key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> \
            Union[str, bytes, int, float]:
        """Retrieve data from Redis by key."""
        data = self._redis.get(key)
        if data is None:
            return data
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Retrieve a string from Redis."""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieve an integer from Redis."""
        value = self.get(key)
        if value is not None:
            try:
                return int(value.decode("utf-8"))
            except (ValueError, TypeError):
                pass
        return None

    @classmethod
    def replay(cls, method: Callable):
        """Display the history of calls of a function."""
        instance = method.__self__
        method_name = method.__qualname__
        inputs_key = f"{method_name}:inputs"
        outputs_key = f"{method_name}:outputs"
        inputs = instance._redis.lrange(inputs_key, 0, -1)
        outputs = instance._redis.lrange(outputs_key, 0, -1)
        print(f"{method_name} was called {len(inputs)} times:")
        for input_str, output_str in zip(inputs, outputs):
            print(f"{method_name}({input_str.decode('utf-8')}) -> \
                    {output_str.decode('utf-8')}")
