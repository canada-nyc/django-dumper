from django.test import TestCase
from django.test.client import Client

from .models import SimpleModel, RelatedModel
from .utils import clear_all_caches


class BaseModelTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.instance = self.model.objects.create()
        self.url = self.instance.get_absolute_url()
        self.access_instance = lambda: self.c.get(self.url)
        self.assert_responses_not_equal = lambda first, second: self.assertNotEqual(first.content, second.content)


class SimpleModelTest(BaseModelTest):
    model = SimpleModel

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

    def tearDown(self):
        clear_all_caches()


class RelatedModelTest(BaseModelTest):
    model = RelatedModel

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

    def tearDown(self):
        clear_all_caches()
