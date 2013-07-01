from django.test import TestCase
from django.core.cache import get_cache
from django.test.utils import override_settings

from dumper import invalidation
from .utils import clear_all_caches


class InalidatePathsTest(TestCase):

    def _test_path_invalidated(self, cache_alias):
        cache = get_cache('default')
        paths = ['/path']
        keys = invalidation.keys_from_paths(paths)
        for key in keys:
            cache.set(key, True)
        invalidation.invalidate_paths(paths)
        for key in keys:
            self.assertFalse(cache.get(key))

    def test_default_cache_invalidated(self):
        self._test_path_invalidated('default')

    @override_settings(CACHE_MIDDLEWARE_ALIAS='other')
    def test_other_cache_invalidated(self):
        self._test_path_invalidated('other')

    def test_paths_not_set_no_error(self):
        paths = ['/path']
        invalidation.invalidate_paths(paths)

    def tearDown(self):
        clear_all_caches()
