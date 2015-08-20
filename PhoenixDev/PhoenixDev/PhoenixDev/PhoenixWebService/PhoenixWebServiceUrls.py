from django.conf.urls import patterns, include, url
from PhoenixDev.PhoenixWebService.Product import views as ProductViews
from PhoenixDev.PhoenixWebService.User import views as UserViews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'phoenix.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # we will reusage signup, because the functionality is same
    url(r'^user/signup/resendopt/$', UserViews.signup),

    url(r'^user/signup/optvalidation/$', UserViews.signup_optvalidation),
    url(r'^user/signup/password/$', UserViews.signup_password),
    url(r'^user/signup/$', UserViews.signup),
    #url(r'/user/login', UserViews.login),
    #url(r'/user/logout', UserViews.logout),
    #url(r'/user/profile/view', UserViews.profile_view),
    #url(r'/user/profile/edit', UserViews.profile_edit),
    
    url(r'^product_ratings/(?P<product_id>[0-9]+)/', ProductViews.product_ratings),
    
)
