import django

try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

from . import views

urlpatterns = [
    url(
        r'^simple/(?P<slug>[-\w]+)/$',
        views.simple_detail,
        name='simple-detail'
    ),
    url(
        r'^related/(?P<slug>[-\w]+)/$',
        views.related_detail,
        name='related-detail'
    ),
    url(
        r'^related-to-generic/(?P<slug>[-\w]+)/$',
        views.related_to_generic_detail,
        name='related-to-generic-detail'
    )
]

if django.VERSION < (1, 8, 0):
    try:
        from django.conf.urls import patterns
    except ImportError:
        from django.conf.urls.defaults import patterns
    urlpatterns = patterns('', *urlpatterns)
