from django.test import TestCase
from django.test.utils import override_settings

from dumper import invalidation


class GetInvalidationKeyTest(TestCase):
    def test_two_paths_different(self):
        paths = ['/path', '/other_path']
        keys = map(invalidation.get_invalidation_key, paths)
        self.assertNotEqual(*keys)

    def test_pound_sign_same(self):
        paths = ['/path', '/path#dsfs']
        keys = map(invalidation.get_invalidation_key, paths)
        self.assertEqual(*keys)

    @override_settings(APPEND_SLASH=False)
    def test_without_append_slash_different(self):
        paths = ['/path', '/path/']
        keys = map(invalidation.get_invalidation_key, paths)
        self.assertNotEqual(*keys)

    @override_settings(APPEND_SLASH=True)
    def test_with_append_slash_same(self):
        paths = ['/path', '/path/']
        keys = map(invalidation.get_invalidation_key, paths)
        self.assertEqual(*keys)
