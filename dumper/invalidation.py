from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.middleware.cache import CacheMiddleware


def invalidate_paths(paths):
    '''
    invalidate that keys for certain paths that the cache middleware would
    cache that get page at.
    '''
    cache_keys = map(key_from_path, paths)
    get_cache().delete_many(cache_keys)


def get_cache():
    '''Returns the cache that is used for URL caching'''
    return CacheMiddleware().cache


def get_key_prefix():
    '''Returns the proper prefix for the URL caching keys'''
    return CacheMiddleware().key_prefix


def get_request_from_path(path):
    '''Returns a request from a path to be used to invalidate that path'''
    request = HttpRequest()
    request.path = path
    return request


def key_from_path(path):
    '''
    Returns the proper cache key based on a path that the cache middleware
    would use for a GET request.
    '''
    request = get_request_from_path(path)
    return get_cache_key(
        request,
        key_prefix=get_key_prefix(),
        cache=get_cache()
    )
