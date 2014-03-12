from django.test import TestCase

from dumper.logging_utils import BaseLogger


class BaseLoggerTest(TestCase):

    def test_unicode_path(self):
        BaseLogger._cache_action(action='', path=u'\u2026')
