from django.conf.urls import patterns, include, url

urlpatterns = patterns('responsive_images.views',
    url(r'adapt-image$', 'adapt_image', name='adapt-image'),
)
