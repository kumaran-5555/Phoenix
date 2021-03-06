﻿from django.conf.urls import patterns, include, url
from PhoenixDev.PhoenixWebService.Product import views as ProductViews
from PhoenixDev.PhoenixWebService.User import views as UserViews
from PhoenixDev.PhoenixWebService.Seller import views as SellerViews
from PhoenixDev.PhoenixWebService.Bargain import views as BargainViews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'phoenix.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # we will reusage signup, because the functionality is same
    url(r'^seller/signup/resendotp/$', SellerViews.signup),
    url(r'^seller/signup/otpvalidation/$', SellerViews.signup_optvalidation),
    url(r'^seller/signup/password/$', SellerViews.signup_password),
    url(r'^seller/signup/$', SellerViews.signup),
    url(r'^seller/login/$', SellerViews.login),
    url(r'^seller/logout/$', SellerViews.logout),
    url(r'^seller/forgotpassword/$', SellerViews.forgot_password),
    url(r'^seller/resetpassword/$', SellerViews.reset_password),

    


    url(r'^user/signup/resendotp/$', UserViews.signup),
    url(r'^user/signup/otpvalidation/$', UserViews.signup_optvalidation),
    url(r'^user/signup/password/$', UserViews.signup_password),
    url(r'^user/signup/$', UserViews.signup),
    url(r'^user/login/$', UserViews.login),
    url(r'^user/logout/$', UserViews.logout),
    url(r'^user/forgotpassword/$', UserViews.forgot_password),
    url(r'^user/resetpassword/$', UserViews.reset_password),
    
    

    #url(r'/user/profile/view', UserViews.profile_view),
    #url(r'/user/profile/edit', UserViews.profile_edit),
    url(r'^product/details/$', ProductViews.product_specs, name='product_specs'),
    url(r'^product/list/$', ProductViews.product_list, name='product_list'),
    url(r'^product/reviews/$', ProductViews.product_reviews, name='product_reviews'),
    url(r'^product/search/$',ProductViews.product_search,name='product_search'),
    url(r'^user/rateproduct/$', ProductViews.rate_product),
    url(r'^user/reviewproduct/$', ProductViews.review_product),
    url(r'^seller/offerings/add/$', BargainViews.add_offerings, name='add_offerings'),
    url(r'^seller/offerings/delete/$', BargainViews.delete_offerings, name='offerings_delete'),


    # messages
    url(r'^user/messages/send/$', BargainViews.send, name='send'),
    url(r'^user/messages/close/$', BargainViews.close, name='close'),
    url(r'^user/messages/viewsummary/$', BargainViews.view_summary, name='view_summary'),
    url(r'^user/messages/viewdetails/$', BargainViews.view_details, name='view_details'),
    url(r'^seller/messages/reply/$', BargainViews.reply, name='reply'),
    url(r'^seller/messages/viewdetails/$', BargainViews.seller_view_details, name='seller_view_details')
    
    
)
