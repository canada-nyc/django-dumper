import dumper.utils
from dumper.logging_utils import InvalidationLogger


def invalidate_paths(paths):
    '''
    Invalidate all pages for a certain path.
    '''
    for path in paths:
        for key in all_cache_keys_from_path(path):
            InvalidationLogger.invalidate(path, key)
            dumper.utils.cache.delete(key)


def all_cache_keys_from_path(path):
    '''
    Each path can actually have multiple cached entries, varying based on different HTTP
    methods. So a GET request will have a different cached response from a HEAD request.
    
    In order to invalidate a path, we must first know all the different cache keys that the
    path might have been cached at. This returns those keys
    '''
    return [dumper.utils.cache_key(path, method) for method in dumper.settings.CACHABLE_METHODS]
