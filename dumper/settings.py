from django.conf import settings


middleware_alias = getattr(settings, 'DUMPER_MIDDLEWARE_ALIAS', 'default')
key_prefix = getattr(settings, 'DUMPER_MIDDLEWARE_KEY_PREFIX', 'dumper.cached_path.')
