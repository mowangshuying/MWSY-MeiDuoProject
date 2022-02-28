from itertools import count
from django.shortcuts import render,redirect
from django.views import View
from django import http
import re,json, logging
from django.db import DatabaseError
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData
from . import constants


# 创建日志输出器
logger = logging.getLogger('django')


#此检查检测应解析但不解析的名称。由于动态分派和duck类型，在有限但有用的情况下，
# 这是可能的。顶级和类级项目比实例项目更受支持
from users.models import User
from users.models import Address
from MeiDuoMall.utils.response_code import RETCODE
from MeiDuoMall.utils.views import LoginRequiredMixin

class UpdateTitleAddressView(LoginRequiredMixin, View):
    """设置地址标题"""

    def put(self, request, address_id):
        """设置地址标题"""
        # 接收参数：地址标题
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

        try:
            # 查询地址
            address = Address.objects.get(id=address_id)

            # 设置新的地址标题
            address.title = title
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '设置地址标题失败'})

        # 4.响应删除地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '设置地址标题成功'})

class DefaultAddressView(LoginRequiredMixin, View):
    """设置默认地址"""

    def put(self, request, address_id):
        """设置默认地址"""
        try:
            # 接收参数,查询地址
            address = Address.objects.get(id=address_id)

            # 设置地址为默认地址
            request.user.default_address = address
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '设置默认地址失败'})

        # 响应设置默认地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '设置默认地址成功'})


class UpdateDestroyAddressView(LoginRequiredMixin, View):
    """修改和删除地址"""
    def put(self, request, address_id):
        """修改地址"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')

       # 判断地址是否存在,并更新地址信息
        try:
            Address.objects.filter(id=address_id).update(
                user = request.user,
                title = receiver,
                receiver = receiver,
                province_id = province_id,
                city_id = city_id,
                district_id = district_id,
                place = place,
                mobile = mobile,
                tel = tel,
                email = email
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '更新地址失败'})

        # 构造响应数据
        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应更新地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '更新地址成功', 'address': address_dict})
    
    def delete(self, request, address_id):
        """删除地址"""
        try:
            # 查询要删除的地址
            address = Address.objects.get(id=address_id)

            # 将地址逻辑删除设置为True
            address.is_deleted = True
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除地址失败'})

        # 响应删除地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除地址成功'})


# 创建地址视图
class CreateAddressView(LoginRequiredMixin, View):
    # post 新增一条地址信息
    def post(self, request):
        # 获取用户的地址数量，如果用户数量大于20的话，返回超过数量上限
        count = request.user.addresses.count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return http.JsonResponse({'code':RETCODE.THROTTLINGERR,'errmsg':'超过地址数量上限'})

        # 接收参数
        json_dict = json.loads(request.body.decode())
        # 接收json格式参数
        receiver = json_dict.get('receiver')
        #获取省市区的id
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        # 获取地址
        place = json_dict.get('place')
        # 获取手机号
        mobile = json_dict.get('mobile')
        # 获取电话号
        tel = json_dict.get('tel')
        # 获取邮箱
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')

        # 保存地址信息
        try:
            address = Address.objects.create(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )

            # 设置默认地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
            
             # 新增地址成功，将新增的地址响应给前端实现局部刷新
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }

            # 响应保存结果
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功', 'address': address_dict})
            
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增地址失败'})


class UsernameCountView(View):
    def get(self,request,username):
        # 接收参数 校验参数
        count = User.objects.filter(username=username).count()

        # 返回结果
        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'OK','count':count})


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
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            return  render(request,'register.html',{'register_errmsg':'注册失败'})

        login(request,user)

        # 响应结果:重定向到首页
        # return http.HttpResponse('注册成功！重定向到首页!')
        # return redirect('/')
        # 通过命名空间重定向
        return redirect(reverse('contents:index'))


class LoginView(View):
    def get(self,request):
        # 直接跳转到登录页面
        return render(request,'login.html')

    def post(self,request):
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        print('username:',username,'password:',password,
              'remembered:',remembered)

        if not all([username,password]):
            return http.HttpResponseForbidden('缺少必须传入的参数')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}',username):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}', password):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')

        # 验证用户名和密码 authenticate所在的包
        user = authenticate(username=username, password=password)

        # 该用户没有注册
        if user is None:
            return  render(request,'login.html',{'account_errmsg': '用户名或密码错误'})

        # 实现状态保持
        login(request,user)

        if remembered != 'on':
            #会话结束后，过期
            request.session.set_expiry(0)
        else:
            # 记住用户的话，none表示两周后过期
            request.session.set_expiry(None)


        next = request.GET.get('next')
        if next:
            # 重定向到next
            response = redirect(next)
        else:
            # 重定向到首页
            response = redirect(reverse('contents:index'))


        # 设置cookie及过期时间
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        return response


class LogoutView(View):
    def get(self,request):
        # 实现退出登录的逻辑
        logout(request)
        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response


class UserInfoView(LoginRequiredMixin,View):

    # 用户中心
    def get(self, request):
        # if request.user.is_authenticated:
        #     return render(request,'user_center_info.html')
        # else:
        #     return redirect(reverse('users:login'))

        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }

        print('UserInfoView::get context:', context)

        return render(request, 'user_center_info.html', context)

    def post(self,request):
        pass


class EmailView(LoginRequiredMixin, View):

    """添加邮箱"""
    def put(self, request):
        # 接收参数
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get('email')

        # json 打印输出
        print('json_dict:', json_dict)

        # 校验参数
        if not email:
            return http.HttpResponseForbidden('缺少email参数')
        
        # 验证邮箱格式是否正确
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')

        # 将用户传入邮箱保存到用户数据表的email字段中
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logging.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})

        verify_url = self.generate_verify_email_url(request.user)
        self.send_verify_email(email,verify_url)

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})

    def generate_verify_email_url(self,user):
        """
        生成验证邮箱的url
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        data = {'user_id': user.id, 'email': user.email}
        token = serializer.dumps(data).decode()
        verify_url = 'http://localhost:8080/emails/verification/?token=' + token
        print('verify_url:',verify_url)
        return verify_url

    def send_verify_email(self, to_email, verify_url):
        """
        发送验证邮箱邮件
        :param to_email: 收件人邮箱
        :param verify_url: 验证链接
        :return: None
        """
        subject = "美多商城邮箱验证"
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
        send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)

class VerifyEmailView(View):
    def get(self, request):
        """实现邮箱验证逻辑"""
        # 接收参数
        token = request.GET.get('token')
        print('token:',token)
        # 校验参数：判断token是否为空和过期，提取user
        if not token:
            return http.HttpResponseBadRequest('缺少token')

        user = self.check_verify_email_token(token)
        # print(user)
        if not user:
            return http.HttpResponseForbidden('无效的token')

        # 修改email_active的值为True
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活邮件失败')

        # 返回邮箱验证结果
        return redirect(reverse('users:info'))
    
    def check_verify_email_token(self,token):
        """
        验证token并提取user
        :param token: 用户信息签名后的结果
        :return: user, None
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            user_id = data.get('user_id')
            email = data.get('email')
            try:
                user = User.objects.get(id=user_id, email=email)
            except User.DoesNotExist:
                return None
            else:
                return user
            

class AdressView(LoginRequiredMixin,View):
    def get(self,request):
        login_user = request.user
        addresses = Address.objects.filter(user=login_user, is_deleted=False)

        address_dict_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_dict_list.append(address_dict)
            

        context = {
            'default_address_id': login_user.default_address_id,
            'addresses': address_dict_list,
        }

        return render(request, 'user_center_site.html', context)