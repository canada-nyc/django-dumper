from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings

from . import models, utils


class BaseModelTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.instance = self.model.objects.create()
        self.url = self.instance.get_absolute_url()
        self.access_instance = lambda: self.c.get(self.url)

        def assert_responses_not_equal(first, second):
            return self.assertNotEqual(first.content, second.content)
        self.assert_responses_not_equal = assert_responses_not_equal

    def tearDown(self):
        utils.clear_all_caches()


class SimpleModelTest(BaseModelTest):
    model = models.SimpleModel

    def test_original_query(self):
        with self.assertNumQueries(1):
            self.access_instance()

    def test_cache_works(self):
        self.access_instance()
        with self.assertNumQueries(0):
            self.access_instance()

    def test_query_after_save(self):
        self.access_instance()
        self.instance.save()
        with self.assertNumQueries(1):
            self.access_instance()

    def test_cache_works_invalidated_after_save(self):
        utils.clear_all_caches()
        with self.assertNumQueries(1):
            self.access_instance()
        with self.assertNumQueries(0):
            self.access_instance()

    @override_settings(DUMPER_PATH_IGNORE_REGEX=r'^/simple/')
    def test_wont_cache_ignored(self):
        self.access_instance()
        with self.assertNumQueries(1):
            self.access_instance()

    def test_wont_used_cached_version_if_path_ignored(self):
        '''
        Even if a path is ignored, we need to make sure that it not only will
        not save a cache for that path, but also not use any left over cached
        version of the path that were created before changing the setting.
        '''
        self.access_instance()

        with self.settings(DUMPER_PATH_IGNORE_REGEX=r'^/simple/'):
            with self.assertNumQueries(1):
                self.access_instance()


class RelatedModelTest(BaseModelTest):
    model = models.RelatedModel

    def test_original_query(self):
        with self.assertNumQueries(2):
            self.access_instance()

    def test_cache_works(self):
        self.access_instance()
        with self.assertNumQueries(0):
            self.access_instance()

    def test_query_after_save(self):
        self.access_instance()
        self.instance.save()
        with self.assertNumQueries(2):
            self.access_instance()

    def test_add_related_invalidate(self):
        first = self.access_instance()
        self.instance.related.create()
        with self.assertNumQueries(2):
            second = self.access_instance()
        self.assert_responses_not_equal(first, second)

    def test_remove_related_invalidate(self):
        related = self.instance.related.create()
        first = self.access_instance()
        self.instance.related.remove(related)
        with self.assertNumQueries(2):
            second = self.access_instance()
        self.assert_responses_not_equal(first, second)

    def test_delete_related_invalidate(self):
        related = self.instance.related.create()
        first = self.access_instance()
        related.delete()
        with self.assertNumQueries(2):
            second = self.access_instance()
        self.assert_responses_not_equal(first, second)

    def test_update_related_invalidate(self):
        related = self.instance.related.create()
        related.slug = 'different_slug'
        related.save()
        first = self.access_instance()
        related.delete()
        with self.assertNumQueries(2):
            second = self.access_instance()
        self.assert_responses_not_equal(first, second)


class RelatedToGenericModelTest(BaseModelTest):
    model = models.RelatedToGenericModel

    def test_original_query(self):
        with self.assertNumQueries(2):
            self.access_instance()

    def test_cache_works(self):
        self.access_instance()
        with self.assertNumQueries(0):
            self.access_instance()

    def test_create_invalidates(self):
        first = self.access_instance()
        models.GenericRelationModel.objects.create(
            content_object=self.instance
        )
        with self.assertNumQueries(2):
            second = self.access_instance()
        self.assert_responses_not_equal(first, second)

    def test_remove_invalidates(self):
        models.GenericRelationModel.objects.create(
            content_object=self.instance
        )
        first = self.access_instance()
        self.instance.generic_related = []
        with self.assertNumQueries(2):
            second = self.access_instance()
        self.assert_responses_not_equal(first, second)

    def test_update_invalidates(self):
        generic = models.GenericRelationModel.objects.create(
            content_object=self.instance
        )
        first = self.access_instance()
        generic.slug = 'another slug'
        generic.save()
        with self.assertNumQueries(2):
            second = self.access_instance()
        self.assert_responses_not_equal(first, second)
