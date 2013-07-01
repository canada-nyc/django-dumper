from django.conf import settings
from django.core.cache import get_cache


def clear_all_caches():
    for cache_alias in settings.CACHES.keys():
        get_cache(cache_alias).clear()
