from django.utils.cache import _generate_cache_header_key
from django.middleware.cache import FetchFromCacheMiddleware

from .invalidation import get_invalidation_key


class InvalidateCacheMiddleware(FetchFromCacheMiddleware):
    """
    Request-phase middleware invalidates the cache for this page.

    Must be used alonside the two-part update/fetch cache middleware.
    InvalidateCacheMiddleware must be before FetchFromCacheMiddleware so that
    it can invalidate the cache before it is returned. Place it directly before
    in that middleware in MIDDLEWARE_CLASSES so that it'll get called next to
    last during the response phase.
    """
    def process_request(self, request):
        invalidation_key = get_invalidation_key(request.path)

        # this is a list of already invalidated requests at this path
        # the values in the last are different header_keys for different
        # requests
        already_invalidated_list = self.cache.get(invalidation_key, [])
        header_key = _generate_cache_header_key(self.key_prefix, request)
        if header_key in already_invalidated_list:
            # if it has already been invalidated then continue on
            # to the cache middleware so it can return the cached content
            return None
        # add this header key to the list of invalidated header keys
        already_invalidated_list.append(header_key)
        # remove the cache for this header key so that the cache middleware
        # will not get the cache and will save a new cache to taht key
        self.cache.set_many({
            header_key: None,
            invalidation_key: already_invalidated_list
        })
