from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 此处本来是 name='users',运行不通过，
    # 修改为MeiDuoMall.apps.users
    name = 'MeiDuoMall.apps.users'
