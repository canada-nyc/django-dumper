from django.test import TestCase

import dumper.invalidation
import dumper.utils


class InvalidatePathsTest(TestCase):
    def setUp(self):
        self.path = '/path'
        self.cache_keys = dumper.invalidation.all_cache_keys_from_path(self.path)

    def test_all_paths_invalidated(self):
        for key in self.cache_keys:
            dumper.utils.cache.set(key, True)
        dumper.invalidation.invalidate_paths([self.path])

        key_values = map(dumper.utils.cache.get, self.cache_keys)
        self.assertFalse(any(key_values))


class AllCacheKeysFromPathTest(TestCase):
    def setUp(self):
        self.path = '/path'

    def test_get_key_returned(self):
        keys = dumper.invalidation.all_cache_keys_from_path(self.path)
        get_method_key = dumper.utils.cache_key(path=self.path, method='GET')
        self.assertIn(get_method_key, keys)
