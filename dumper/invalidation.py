import hashlib

from django.core.cache import get_cache
from django.conf import settings


def invalidate_paths(paths):
    '''
    invalidate that keys for certain paths that the cache middleware would
    cache that get page at.
    '''
    keys = map(get_path_key, paths)
    cache = get_cache(settings.CACHE_MIDDLEWARE_ALIAS)
    cache.delete_many(keys)


def get_path_key(path):
    path = path.split('#')[0]
    if settings.APPEND_SLASH and not path.endswith('/'):
        path += '/'
    key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
    path = hashlib.md5(path)
    cache_key = 'dumper.invalidation.invalidate_paths.{0}.{1}'.format(
        key_prefix, path.hexdigest()
    )
    return cache_key
