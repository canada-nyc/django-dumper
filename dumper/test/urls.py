from .views import detail
try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    '',
    url(
        r'^(?P<slug>[-\w]+)/$',
        detail,
        name='detail'
    )
)
