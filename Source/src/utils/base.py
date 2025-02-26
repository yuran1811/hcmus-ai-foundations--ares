import functools
from datetime import datetime
from typing import Callable


def manhattan(x1: int, y1: int, x2: int, y2: int):
    return abs(x1 - x2) + abs(y1 - y2)


def get_timestamp() -> str:
    return datetime.now().strftime("%H:%M:%S, %d.%m.%y")


def split_into_chunks(arr, chunk_size: int):
    return [arr[i : i + chunk_size] for i in range(0, len(arr), chunk_size)]


def byte_convert(num: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024.0

    return f"{num:.2f} PB"


def memoize(fn: Callable, slot=None, maxsize=128):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""

    if slot:

        def memoized_f(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val

        return memoized_f

    @functools.lru_cache(maxsize=maxsize)
    def memoized_fn(*args):
        return fn(*args)

    return memoized_fn
