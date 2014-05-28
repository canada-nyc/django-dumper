# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from dumper.logging_utils import BaseLogger


class BaseLoggerTest(TestCase):

    def setUp(self):
        self.logger = BaseLogger
        self.logger.module = 'test.test_logging_utils'

    def test_unicode_path(self):
        self.logger._cache_action(action='', path='’')
