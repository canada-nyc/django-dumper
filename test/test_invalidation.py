from django.test import TestCase

from dumper import invalidation


class GetInvalidationKeyTest(TestCase):
    def test_two_paths_different(self):
        paths = ['/path', '/other_path']
        keys = map(invalidation.get_invalidation_key, paths)
        self.assertNotEqual(*keys)
