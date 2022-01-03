"""美多商城URL的配置信息

“urlpatterns”列表将URL路由到视图。有关更多信息，请参阅:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #users
    # url(r'',include('users.urls',namesapce='users')是错误的
    # 下面这个才是正确的
    url(r'',include(('users.urls','users'),namespace='users')),
    # 添加contents子应用的相关内容
    url(r'',include(('contents.urls','contents'),namespace='contents')),
]
