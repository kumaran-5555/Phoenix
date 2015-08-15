from django.conf.urls import patterns, include, url
import PhoenixWebService.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'phoenix.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^product_ratings/(?P<product_id>[0-9]+)', PhoenixWebService.views.productRatings),
    
)
