from .base import *

ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testdb',
        'USER': 'wlsdn2749',
        'PASSWORD': 'asdf0313',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS':{
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}