from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
import PhoenixWebService.views
import PhoenixWebService.PhoenixWebServiceUrls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'phoenix.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^web/', include(PhoenixWebService.PhoenixWebServiceUrls)),
    url(r'^home/', PhoenixWebService.views.index),
    url(r'^admin/', include(admin.site.urls)),
)
