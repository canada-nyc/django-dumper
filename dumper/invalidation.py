from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.middleware.cache import CacheMiddleware


def invalidate_paths(paths):
    cache_keys = map(keys_from_paths, paths)
    CacheMiddleware().cache.delete_many(cache_keys)


def keys_from_paths(paths):
    for path in paths:
        request = HttpRequest()
        request.path = path
        yield get_cache_key(
            request,
            key_prefix=CacheMiddleware().key_prefix,
            cache=CacheMiddleware().cache
        )
