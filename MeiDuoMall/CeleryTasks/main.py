# CeleryTasks的入口

from celery import Celery
"""
创建Celery实例
"""
celeryApp = Celery('meiduo')

celeryApp.config_from_object('CeleryTasks.config')


