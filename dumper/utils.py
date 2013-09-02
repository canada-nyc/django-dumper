import hashlib
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

from django.core.cache import get_cache

import dumper.settings


def cache_key(path, method):
    # remove fragment from path
    path = urlsplit(path)[2]

    path_hash = hashlib.md5(path.encode('utf-8')).hexdigest()

    return '{prefix}{path_hash}.{method}'.format(
        prefix=dumper.settings.KEY_PREFIX,
        path_hash=path_hash,
        method=method
    )


def cache_key_from_request(request):
    return cache_key(request.path, request.method)

cache = get_cache(dumper.settings.CACHE_ALIAS)
