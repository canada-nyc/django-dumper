from django.test import TestCase

from dumper.utils import cache_key


class CacheKeyTest(TestCase):
    def test_two_paths_different(self):
        paths = ['/path', '/other_path']
        keys = map(cache_key, paths, ['', ''])
        self.assertNotEqual(*keys)

    def test_fragement_removed(self):
        paths = ['/path', '/path#dsfs']
        keys = map(cache_key, paths, ['', ''])
        self.assertEqual(*keys)

    def test_two_methods_different(self):
        paths = ['HEAD', 'GET']
        keys = map(cache_key, ['', ''], paths)
        self.assertNotEqual(*keys)
