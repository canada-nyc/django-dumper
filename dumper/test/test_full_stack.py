from django.test import TransactionTestCase
from django.test.client import Client

from .models import SimpleModel
from .utils import clear_all_caches


class SimpleModelTest(TransactionTestCase):
    def setUp(self):
        self.c = Client()
        self.model = SimpleModel.objects.create()
        self.url = self.model.get_absolute_url()
        self.access_model = lambda: self.c.get(self.url)

    def test_original_query(self):
        with self.assertNumQueries(1):
            self.access_model()

    def test_no_queries(self):
        self.access_model()
        with self.assertNumQueries(0):
            self.access_model()

    def test_query_after_save(self):
        self.access_model()
        self.model.save()
        with self.assertNumQueries(1):
            self.access_model()

    def tearDown(self):
        clear_all_caches()
