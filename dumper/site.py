from django.db.models import signals

from .invalidation import invalidate_paths


def register(model):
    def invalidate_model_paths(sender, instance, **kwargs):
        paths = instance.dependent_paths()
        invalidate_paths(paths)

    signals.post_save.connect(invalidate_model_paths)
    signals.pre_delete.connect(invalidate_model_paths)
