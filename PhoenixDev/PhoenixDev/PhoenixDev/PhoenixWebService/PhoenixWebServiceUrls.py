from django.conf.urls import patterns, include, url
from PhoenixDev.PhoenixWebService.Product import views as ProductViews
from PhoenixDev.PhoenixWebService.User import views as UserViews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'phoenix.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # we will reusage signup, because the functionality is same
    url(r'^user/signup/resendotp/$', UserViews.signup),

    url(r'^user/signup/otpvalidation/$', UserViews.signup_optvalidation),
    url(r'^user/signup/password/$', UserViews.signup_password),
    url(r'^user/signup/$', UserViews.signup),
    url(r'^user/login/$', UserViews.login),
    url(r'^user/logout/$', UserViews.logout),
    #url(r'/user/profile/view', UserViews.profile_view),
    #url(r'/user/profile/edit', UserViews.profile_edit),
    url(r'^product/details/$', ProductViews.product_specs, name='product_specs'),
    url(r'^product/list/$', ProductViews.product_list, name='product_list'),
    #url(r'^product_ratings/(?P<product_id>[0-9]+)/', ProductViews.product_ratings),
    url(r'^user/rateproduct/$', ProductViews.rate_product),
    url(r'^user/reviewproduct/$', ProductViews.review_product),
    
)
