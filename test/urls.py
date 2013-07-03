try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from . import views


urlpatterns = patterns(
    '',
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
)
