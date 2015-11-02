from django.conf import settings
try:  # new import introduced in Django 1.7
    from django.core.cache import caches
    get_cache = lambda c: caches[c]
except ImportError:
    from django.core.cache import get_cache


def clear_all_caches():
    for cache_alias in settings.CACHES.keys():
        get_cache(cache_alias).clear()
