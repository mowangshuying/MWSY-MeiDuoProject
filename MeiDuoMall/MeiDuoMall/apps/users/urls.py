from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    #url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5-20})/count/$',
        #views.UsernameCountView.as_view()),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',views.UsernameCountView.as_view()),
    # 用户登录
    url(r'^login/$',views.LoginView.as_view(),name='login'),
]
