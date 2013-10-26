import re

import dumper.settings
import dumper.utils
from dumper.logging_utils import MiddlewareLogger


class FetchFromCacheMiddleware(object):
    """
    Request-phase middleware that checks to make sure this cache has been
    regenerated if it was invalidated.

    Must be used in place of FetchFromCacheMiddleware.
    """

    def should_retrieve_cache(self, request):
        return not re.match(dumper.settings.PATH_IGNORE_REGEX(), request.path)

    def process_request(self, request):
        if self.should_retrieve_cache(request):
            key = dumper.utils.cache_key_from_request(request)
            value = dumper.utils.cache.get(key)
            MiddlewareLogger.get(key, value, request)
            return value
        else:
            MiddlewareLogger.not_get(request)


class UpdateCacheMiddleware(object):
    """
    Response-phase cache middleware that updates the cache if the response is
    cacheable and adds the cache key to the regenerated caches.

    Must be used in place of UpdateCacheMiddleware.
    """
    def should_cache(self, request, response):
        return all([
            request.method in dumper.settings.CACHABLE_METHODS,
            response.status_code in dumper.settings.CACHABLE_RESPONSE_CODES,
            not re.match(dumper.settings.PATH_IGNORE_REGEX(), request.path)
        ])

    def process_response(self, request, response):
        if self.should_cache(request, response):
            key = dumper.utils.cache_key_from_request(request)
            MiddlewareLogger.save(key, request)
            dumper.utils.cache.set(key, response)
        else:
            MiddlewareLogger.not_save(request)
        return response
