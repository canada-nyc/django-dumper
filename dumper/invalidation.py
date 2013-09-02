import hashlib
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit
from django.core.cache import get_cache
from django.conf import settings

from .settings import middleware_alias, key_prefix


def invalidate_paths(paths):
    '''
    Invlidate all the paths in the cache.
    '''
    keys = map(get_path_key, paths)
    cache = get_cache(middleware_alias)
    cache.delete_many(keys)


def get_path_key(path):
    path = urlsplit(path)[2]
    if settings.APPEND_SLASH and not path.endswith('/'):
        path += '/'
    path = hashlib.md5(path.encode('utf-8'))
    cache_key = 'dumper.invalidation.invalidate_paths.{0}.{1}'.format(
        key_prefix, path.hexdigest()
    )
    return cache_key
