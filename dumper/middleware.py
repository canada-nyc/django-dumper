from django.middleware import cache
from django.utils.cache import _generate_cache_header_key, _generate_cache_key

from .invalidation import get_path_key


class FetchFromCacheMiddleware(cache.FetchFromCacheMiddleware):
    """
    Request-phase middleware that checks to make sure this cache has been
    regenerated if it was invalidated.

    Must be used in place of FetchFromCacheMiddleware.
    """
    def process_request(self, request):
        # Each path can be invalidated by deleting this key. It is only
        # based on the request path, meaning that if you delete this key
        # than all requests to this path will be regenerated in the cache
        path_key = get_path_key(request.path)
        # the different requests that already have been regenerated
        # are saved in a dictionary structure.
        already_regenerated = self.cache.get(path_key, {})
        # the keys in this dictionary are header keys. These keys are
        # dependent upon two things besides the path. These are query
        # strings and location headers set by the location middleware.
        # so `/path?hi=ho` would have a different header key than
        # `/path`.
        header_key = _generate_cache_header_key(self.key_prefix, request)
        # The cache middleware stores a list of headers that
        # the request should vary on at this cache key
        header_list = self.cache.get(header_key, None)
        # If the cached value returned by this key is None, that means that
        # the different pages at this header key have never been cached before.
        if header_list is None:
            # That means that all of the different pages at this header key
            # need to be regenerated. So empty the list of pages that
            # already have been regenerated at this path
            already_regenerated[header_key] = []
            self.cache.set(path_key, already_regenerated)
            request._cache_update_cache = True
            return
        # since the header list has some headers in it, this means that
        # this path has been cached before. the cache key varies based on the
        # request headers specified in the header list and the request method
        cache_key = _generate_cache_key(
            request,
            request.method,
            header_list,
            self.key_prefix
        )
        # get the list of cache keys that already have been invalidated for
        # this cache header
        already_regenerated_cache_keys = already_regenerated.setdefault(
            header_key,  # key
            []  # default
        )
        if cache_key not in already_regenerated_cache_keys:
            # this cache key will be added to the list of already regenerated
            # keys in the update cache middleware
            request._cache_update_cache = True
            return
        # if the cache has already been regenerated
        original_middleware = super(FetchFromCacheMiddleware, self)
        return original_middleware.process_request(request)


class UpdateCacheMiddleware(cache.UpdateCacheMiddleware):
    """
    Response-phase cache middleware that updates the cache if the response is
    cacheable and adds the cache key to the regenerated caches.

    Must be used in place of UpdateCacheMiddleware.
    """
    def process_response(self, request, response):

        original_middleware = super(UpdateCacheMiddleware, self)
        original_response = original_middleware.process_response(
            request,
            response
        )
        if (
            self._should_update_cache(request, response) and
            not response.streaming and
            response.status_code == 200 and
            cache.get_max_age(response)
        ):
            header_key = _generate_cache_header_key(self.key_prefix, request)
            header_list = self.cache.get(header_key)
            cache_key = _generate_cache_key(
                request,
                request.method,
                header_list,
                self.key_prefix
            )
            path_key = get_path_key(request.path)
            already_regenerated = self.cache.get(path_key, {})
            already_regenerated_cache_keys = already_regenerated.setdefault(
                header_key,  # key
                []  # default
            )
            already_regenerated_cache_keys.append(cache_key)
            self.cache.set(path_key, already_regenerated)
        return original_response
