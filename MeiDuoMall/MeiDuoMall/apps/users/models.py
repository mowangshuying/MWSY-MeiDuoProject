from django.db import models
from django.contrib.auth.models import AbstractUser



# 在此处创建模型
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
    

class Address(models.Model):
    """用户地址"""
    # 用户
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    # 地址名称
    title = models.CharField(max_length=20, verbose_name='地址名称')
    # 收货人
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    # 地址
    place = models.CharField(max_length=50, verbose_name='地址')
    # 手机
    mobile = models.CharField(max_length=11, verbose_name='手机')
    # 固定电话
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    # 电子邮箱
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    # 是否删除
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 更新时间
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']



