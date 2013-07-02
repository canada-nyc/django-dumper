from six import string_types

from django.db.models import signals

from .invalidation import invalidate_paths


def register(model):
    register_instance_function_at_save(model, invalidate_model_paths)


def register_instance_function_at_save(model, function):

    def save_function(sender, instance, **kwargs):
        function(instance)

    signals.post_save.connect(save_function, model, weak=False)
    signals.pre_delete.connect(save_function, model, weak=False)


def get_paths_from_model(model):
    paths = model.dependent_paths()
    if isinstance(paths, string_types):
        model_name = model.__class__.__name__
        raise TypeError(
            ('dependent_paths on {} should return a list of paths, not a'
             'string'.format(model_name))
        )
    return paths


def invalidate_model_paths(model):
    paths = get_paths_from_model(model)
    invalidate_paths(paths)
