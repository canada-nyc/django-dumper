from mock import Mock

from django.test import TestCase

from dumper import site


class TestGetPathsFromModel(TestCase):

    def model_from_dependent_paths(self, paths):
        model = lambda: None
        model.dependent_paths = Mock(return_value=paths)
        return model

    def test_list_paths(self):
        paths = ['/path']
        model = self.model_from_dependent_paths(paths)
        self.assertEqual(site.get_paths_from_model(model), paths)

    def test_string_path_raises_error(self):
        paths = 'should_be_list'
        model = self.model_from_dependent_paths(paths)
        with self.assertRaises(TypeError):
            site.get_paths_from_model(model)
