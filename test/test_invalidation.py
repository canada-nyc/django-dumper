from django.test import TestCase
from django.core.cache import cache, get_cache

from django.test.utils import override_settings

from dumper import invalidation
from .utils import clear_all_caches


class InalidatePathsTest(TestCase):
    def test_default_cache_invalidated(self):
        path = '/path'
        key = invalidation.key_from_path(path)
        cache.set(key, True)
        self.assertTrue(cache.get(key))
        invalidation.invalidate_paths([path])
        self.assertFalse(cache.get(key))

    def test_paths_not_set_no_error(self):
        paths = ['/path']
        invalidation.invalidate_paths(paths)

    def tearDown(self):
        clear_all_caches()


class RequestFromPathTest(TestCase):
    def test_path_is_correct(self):
        path = '/path'
        request = invalidation.get_request_from_path(path)
        self.assertEqual(request.path, path)


class GetKeyPrefixTest(TestCase):
    def test_no_prefix(self):
        self.assertEqual(
            invalidation.get_key_prefix(),
            ''
        )

    @override_settings(CACHE_MIDDLEWARE_KEY_PREFIX='_')
    def test_other_prefix(self):
        self.assertEqual(
            invalidation.get_key_prefix(),
            '_'
        )


class GetKeyCacheTest(TestCase):
    def test_default_cache(self):
        self.assertEqual(
            invalidation.get_cache()._lock,
            get_cache('default')._lock
        )

    @override_settings(CACHE_MIDDLEWARE_ALIAS='other')
    def test_other_cache(self):
        self.assertEqual(
            invalidation.get_cache()._lock,
            get_cache('other')._lock
        )


class KeyFromPathTest(TestCase):
    def test_path(self):
        path = '/path'
        request = invalidation.get_request_from_path(path)
        key = invalidation.get_cache_key(request)
        self.assertEqual(invalidation.key_from_path(path), key)
