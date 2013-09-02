import dumper.utils


def invalidate_paths(paths):
    '''
    Invalidate all pages for a certain path.
    '''
    for path in paths:
        for key in all_cache_keys_from_path(path):
            dumper.utils.cache.delete(key)


def all_cache_keys_from_path(path):
    return [dumper.utils.cache_key(path, method) for method in dumper.settings.CACHABLE_METHODS]
