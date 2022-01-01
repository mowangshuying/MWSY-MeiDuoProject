## MeiDuoProject

#### 介绍
python项目：美多商城，仅仅用于个人的学习，记录学习利用django开发项目的过程等

#### 环境说明

软件列表

```
Package                Version
---------------------- -------
asgiref                3.4.1
Deprecated             1.2.13
Django                 3.2.10
django-redis           5.2.0
importlib-metadata     4.8.3
Jinja2                 3.0.3
MarkupSafe             2.0.1
mysql-connector-python 8.0.27
mysqlclient            1.4.6
packaging              21.3
pip                    21.3.1
PyMySQL                1.0.2
pyparsing              3.0.6
pytz                   2021.3
redis                  4.1.0
setuptools             28.8.0
sqlparse               0.4.2
typing_extensions      4.0.1
wheel                  0.37.1
wrapt                  1.13.3
zipp                   3.6.0
```

安装软件

```关于安装
pip install django==3.2.10
# 其他可以根据也可以设定指定版本
pip install Jinja2
pip install pymysql
pip insatll django-redis

下载并安装mysql8.x
```

注意事项：

django3.x版本不支持mysql5.x,所以我使用的版本为mysql8.x

#### 常用的命令

```
#创建一个项目
python django-admin startproject MeiDuoProject
#启动项目
python manage.py runserver
# 创建子应用
python manage.py startapp users
# 创建迁移文件
python manage.py makemigrations
# 执行迁移命令
python manage.py migrate
```

#### 开发日志

##### 2021/12/28-2022/1/1：

##### 2021/1/1: 

1、mysql8.x的安装包放在doc/soft文件夹下

![image-20220101142407563](./doc/img/image-20220101142407563.png)

2、安装为mysql8.x之后，执行python manage.py migrate没有出错，执行产生的效果图如下：

![image-20220101141845578](./doc/img/image-20220101141845578.png)

#### 问题日志

由于过程中经常遇到各种奇葩问题，所以特此记录。

