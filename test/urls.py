try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from .views import simple_detail, related_detail


urlpatterns = patterns(
    '',
    url(
        r'^simple/(?P<slug>[-\w]+)/$',
        simple_detail,
        name='simple-detail'
    ),
    url(
        r'^related/(?P<slug>[-\w]+)/$',
        related_detail,
        name='related-detail'
    )
)
