
# ../config/settings/base.py

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Загружаем .env
load_dotenv(BASE_DIR / '.env')  # загрузка переменных из .env

'''
Добавляем apps/ в системный путь поиска модулей (sys.path),
Позволяем писать в INSTALLED_APPS и импортировать приложения по коротким именам, например: 'users' вместо 'apps.users'.
'''
sys.path.append(str(BASE_DIR / 'apps'))


# Безопасность
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = []


# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',

    # Локальные
    'apps.core.apps.CoreConfig',
    'apps.users.apps.UsersConfig',
    'apps.main.apps.MainConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # если есть глобальные шаблоны
        'APP_DIRS': True,                   # ключевой момент — поиск в apps/*/templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'

# База данных (в dev и prod отдельная настройка)
DATABASES = {}

# Авторизация
'''
Если применяется кастомная модель, до создания любых миграций,
подготовить к миграции class CustomUser(UUIDModel, AbstractBaseUser, PermissionsMixin)
и произвести при первой миграции, предварительно указав:  AUTH_USER_MODEL =  'users.CustomUser'
чтобы Django понимал, что используется именно ваша модель.
'''
AUTH_USER_MODEL =  'users.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Локализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Minsk'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Статика и медиа
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'assets',
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'static_root'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
