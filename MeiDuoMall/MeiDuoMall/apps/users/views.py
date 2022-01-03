from django.shortcuts import render
from django.views import View
from django import http
import re
from django.db import DatabaseError

#此检查检测应解析但不解析的名称。由于动态分派和duck类型，在有限但有用的情况下，
# 这是可能的。顶级和类级项目比实例项目更受支持
from users.models import User

class RegisterView(View):
    def get(self,request):
        # 提供注册页面
        return render(request,'register.html')

    def post(self,request):
        # 业务逻辑
        # value = request.POST.get('key')
        # print(request.POST)
        #pass

        # 校验参数：前后端校验参数必须要分开，避免恶意用户的前端逻辑，要保证数据校验逻辑相同
        # 判断参数是否齐全 all([列表]) 会去校验列表中元素是否为空，如果有一个为空，返回为false
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        if all([username,password,password2,mobile,allow]) == False:
            return http.HttpResponseForbidden('缺少必要参数')
        # 判断用户名是否是5-20字符
        if re.match(r'^[a-zA-Z_-]{5,20}$',username) == False:
            return http.HttpResponseForbidden('请输入5-20个字符作为用户名')
        # 判断密码是否是8-28字符
        if re.match(r'[a-zA-Z_-]{8,28}$',password) == False:
            return http.HttpResponseForbidden('请输入5-28个字符作为用户密码')
        # 判断两次输入的密码是否相同
        if password!=password2:
            return http.HttpResponseForbidden('两次用户密码不一致')

        # 判断手机号是否合法
        if re.match(r'^1[3-9]\d{9}',mobile) == False:
            return http.HttpResponseForbidden('手机号格式不对')

        # 用户是否勾选了协议
        if allow!='on':
            return  http.HttpResponseForbidden('没有勾选协议')

        # 保存注册业务核心
        try:
            User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            return  render(request,'register.html',{'register_errmsg':'注册失败'})

        # 响应结果:重定向到首页
        return http.HttpResponse('注册成功！重定向到首页!')