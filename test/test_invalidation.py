from django.test import TestCase

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
