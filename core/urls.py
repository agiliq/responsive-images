from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'home', name='home'),
)
