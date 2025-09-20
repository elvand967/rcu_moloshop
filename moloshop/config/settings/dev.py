
# ../config/settings/dev.py

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''
debug_toolbar.middleware.DebugToolbarMiddleware — это middleware, 
который активирует вывод панели инструментов на странице для отладки и анализа работы вашего Django-приложения.
Опционально указывают в base.py список IP-адресов, для которых будет доступна панель 
(часто INTERNAL_IPS = ['127.0.0.1']).
'''
# # Дополнительно можно подключить django-debug-toolbar и прочее
# INSTALLED_APPS += [
#     'debug_toolbar',
# ]
#
# MIDDLEWARE = [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ] + MIDDLEWARE
#
# INTERNAL_IPS = ['127.0.0.1']
