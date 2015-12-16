# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from dumper import logging_utils

from .models import LoggingModel


class BaseLoggerTest(TestCase):

    def setUp(self):
        self.logger = logging_utils.BaseLogger
        self.logger.module = 'test.test_logging_utils'

    def test_unicode_path(self):
        self.logger._cache_action(action='', path='’')


class SiteLoggerTest(TestCase):
    def setUp(self):
        self.logger = logging_utils.SiteLogger

    def test_unicode_invalidate_instance(self):
        instance = LoggingModel.objects.create(text='’')
        logging_utils.SiteLogger.invalidate_instance(instance)
