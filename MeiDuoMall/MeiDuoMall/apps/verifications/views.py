from django.views import View

from django_redis import get_redis_connection
from django import http
from verifications.libs.captcha.captcha import captcha
from MeiDuoMall.MeiDuoMall.utils import constants

# 在此处创建你的视图
class ImageCodeView(View):
    def get(self,request,uuid):
        # 接收和校验参数
        # 生成图形验证码
        text,image = captcha.generate_captcha()
        print('text:',text,'image:',image)
        # 保存图形验证码
        redis_conn = get_redis_connection('virify_code')
        #redis_conn.setex('key','expires','value')
        redis_conn.setex('img_%s'%uuid,constants.IMAGE_CODE_REDIS_EXPIRES,text)

        return http.HttpResponse(image,content_type='image/jepg')


