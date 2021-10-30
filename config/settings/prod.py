from .base import *

ALLOWED_HOSTS = ['13.209.161.6']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'config',
        'USER': 'root',
        'PASSWORD': 'wjsansrk',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS':{
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}