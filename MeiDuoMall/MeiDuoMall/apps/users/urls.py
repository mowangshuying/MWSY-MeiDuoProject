from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    #url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5-20})/count/$',
        #views.UsernameCountView.as_view()),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',views.UsernameCountView.as_view()),
    # 用户登录
    url(r'^login/$',views.LoginView.as_view(),name='login'),
    # 用户退出登录
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # 用户中心
    url(r'^info/$',views.UserInfoView.as_view(),name='info'),
    # 添加邮箱
    url(r'^emails/$',views.EmailView.as_view(),name='emails'),
    # 添加验证邮箱
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    # 展示收货地址
    url(r'^addresses/$',views.AdressView.as_view(),name='address'),
    # 新增用户地址
    url(r'^addresses/create/$', views.CreateAddressView.as_view()),
    # 更新和删除地址
    url(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),
    # 修改默认地址的
    url(r'^addresses/(?P<address_id>\d+)/default/$',views.DefaultAddressView.as_view()),
    # 修改地址标题
    url(r'^addresses/(?P<address_id>\d+)/title/$',views.UpdateTitleAddressView.as_view()),
    
]
