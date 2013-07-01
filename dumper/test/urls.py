from django.conf.urls import patterns, url

from .views import detail


urlpatterns = patterns(
    '',
    url(
        r'^(?P<slug>[-\w]+)/$',
        detail,
        name='detail'
    )
)
