from django.shortcuts import render
from django.views import  View


# 在这里创建你的视图.
class IndexView(View):
    def get(self,request):
        # 提供首页的广告页面
        return render(request,'index.html')
