from django.test import TestCase
from django.test.utils import override_settings

from dumper import invalidation


class GetPathKeyTest(TestCase):
    def test_two_paths_different(self):
        paths = ['/path', '/other_path']
        keys = map(invalidation.get_path_key, paths)
        self.assertNotEqual(*keys)

    def test_fragement_removed(self):
        paths = ['/path', '/path#dsfs']
        keys = map(invalidation.get_path_key, paths)
        self.assertEqual(*keys)

    @override_settings(APPEND_SLASH=False)
    def test_without_append_slash_different(self):
        paths = ['/path', '/path/']
        keys = map(invalidation.get_path_key, paths)
        self.assertNotEqual(*keys)

    @override_settings(APPEND_SLASH=True)
    def test_with_append_slash_same(self):
        paths = ['/path', '/path/']
        keys = map(invalidation.get_path_key, paths)
        self.assertEqual(*keys)
