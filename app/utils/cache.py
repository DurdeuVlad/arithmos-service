from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache as _cache_decorator


def init_cache():
    """
    Initialize the in-memory cache backend for FastAPI-Cache2.
    Call this once on application startup.
    """
    FastAPICache.init(
        backend=InMemoryBackend(),
        prefix="fastapi-cache"
    )


def cache(expire: int):
    """
    Decorator to cache endpoint results for the given expire time (in seconds).
    Usage:
        @cache(expire=60)
        async def endpoint(...):
            ...
    """
    return _cache_decorator(namespace="fastapi-cache", expire=expire)