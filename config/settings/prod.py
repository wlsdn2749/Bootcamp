from .base import *


ALLOWED_HOSTS = [get_secret("ALLOWED_HOST")]

DB_NAME = get_secret("DB_NAME")
DB_USER = get_secret("DB_USER")
DB_PASSWORD = get_secret("DB_PASSWORD")
DB_HOST = get_secret("DB_HOST")
DB_PORT = get_secret("DB_PORT")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS':{
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}