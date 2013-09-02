import django

from os import path


SECRET_KEY = 'not secret'
INSTALLED_APPS = ('dumper', 'test', 'django.contrib.contenttypes')
TEMPLATE_DEBUG = DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}
ROOT_URLCONF = 'test.urls'

# Testing
if django.VERSION[:2] < (1, 6):
    INSTALLED_APPS += ('discover_runner',)
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = path.dirname(path.dirname(__file__))

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'dumper-default'
    },
    'other': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'dumper-other'
    },
}
MIDDLEWARE_CLASSES = (
    'dumper.middleware.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'dumper.middleware.FetchFromCacheMiddleware',
)
