import logging


class BaseLogger(object):
    @classmethod
    def get_logger(cls):
        logger = logging.getLogger(cls.module)
        logger.setLevel('DEBUG')
        return logger

    @classmethod
    def _log(cls, message):
        cls.get_logger().debug(message)

    @classmethod
    def _cache_action(cls, action, path=None, method=None, key=None):
        log_string = action
        if path:
            log_string += ' path "{0}"'.format(path)
        if method:
            log_string += ' with method "{0}"'.format(method)
        if key:
            log_string += ' as key "{0}"'.format(key)
        cls._log(log_string)


class MiddlewareLogger(BaseLogger):
    module = 'dumper.middleware'

    @classmethod
    def get(cls, key, value, request):
        success_text = 'found' if value else 'didnt find'
        cls._cache_action(
            success_text,
            path=request.path,
            method=request.method,
            key=key
        )

    @classmethod
    def not_get(cls, request):
        cls._cache_action(
            'skipped getting',
            path=request.path,
        )

    @classmethod
    def save(cls, key, request):
        cls._cache_action(
            'cached',
            path=request.path,
            method=request.method,
            key=key
        )

    @classmethod
    def not_save(cls, request):
        cls._cache_action(
            'skipped caching',
            path=request.path,
            method=request.method,
        )


class InvalidationLogger(BaseLogger):
    module = 'dumper.invalidation'

    @classmethod
    def invalidate(cls, path, key):
        cls._cache_action(
            'invalidated',
            path=path,
            key=key
        )


class SiteLogger(BaseLogger):
    module = 'dumper.site'

    @classmethod
    def register(cls, model):
        app_name = model._meta.app_label
        model_name = model._meta.object_name
        cls._log('registered {0}.{1}'.format(app_name, model_name))

    @classmethod
    def invalidate_instance(cls, instance):
        instance_name = repr(instance)

        model = instance.__class__
        app_name = model._meta.app_label
        model_name = model._meta.object_name
        cls._log('invalidating instance #{0} "{1}" of {2}.{3}'.format(
            instance.pk,
            instance_name,
            app_name,
            model_name
        ))
