from django.conf import settings


CACHE_ALIAS = getattr(settings, 'DUMPER_CACHE_ALIAS', 'default')
KEY_PREFIX = getattr(settings, 'DUMPER_KEY_PREFIX', 'dumper.cached_path.')
CACHABLE_METHODS = ['HEAD', 'GET']
CACHABLE_RESPONSE_CODES = [200]


def PATH_IGNORE_REGEX():
    return getattr(settings, 'DUMPER_PATH_IGNORE_REGEX', r'^/admin/')
