from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
import Test.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'phoenix.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^home/', Test.views.index),
    url(r'^admin/', include(admin.site.urls)),
)
