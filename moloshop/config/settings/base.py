
# ../config/settings/base.py

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Загружаем .env
load_dotenv(BASE_DIR / ".env")  # загрузка переменных из .env

"""
Добавляем apps/ в системный путь поиска модулей (sys.path),
Позволяем писать в INSTALLED_APPS и импортировать приложения по коротким именам, например: 'users' вместо 'apps.users'.
"""
sys.path.append(str(BASE_DIR / "apps"))

# Безопасность
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 465))
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL= os.getenv('DEFAULT_FROM_EMAIL')

# Приложения
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mptt",
    "nested_admin",
    "widget_tweaks",
    # WYSIWYG-редактор Ckeditor (django-ckeditor)
    "ckeditor",
    "ckeditor_uploader",
    # Локальные
    "apps.core.apps.CoreConfig",
    "apps.users.apps.UsersConfig",
    "apps.main.apps.MainConfig",
    "apps.business.apps.BusinessConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'apps.users.middleware.EmailVerifiedMiddleware',
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # если есть глобальные шаблоны
        "APP_DIRS": True,  # ключевой момент — поиск в apps/*/templates
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Кастомный контекст процессор для работы с меню пользователя
                # Теперь во всех шаблонах будет доступна переменная menu_sections с меню пользователя
                # и current_path для подсветки активного пункта.
                'apps.users.context_processors.user_menu',
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"

# База данных (в dev и prod отдельная настройка)
DATABASES = {}

# Авторизация
"""
Если применяется кастомная модель, до создания любых миграций,
подготовить к миграции class CustomUser(UUIDModel, AbstractBaseUser, PermissionsMixin)
и произвести при первой миграции, предварительно указав:  AUTH_USER_MODEL =  'users.CustomUser'
чтобы Django понимал, что используется именно ваша модель.
"""
AUTH_USER_MODEL = "users.CustomUser"

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Локализация
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Minsk"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Статика и медиа
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "assets",
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "static_root"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# Стандартный backend обработки изображений
CKEDITOR_IMAGE_BACKEND = "pillow"


# Куда складывать загруженные файлы редактора внутри MEDIA_ROOT
CKEDITOR_UPLOAD_PATH = "uploads/"


# Безопасность/ограничения
CKEDITOR_ALLOW_NONIMAGE_FILES = False  # запретить не‑изображения через виджет
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = True  # удобные имена файлов
CKEDITOR_RESTRICT_BY_USER = False  # True — разложить по /uploads/<user_id>/. Включи True, если нужна сегрегация по юзерам


# Конфиги тулбаров/плагинов
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "auto",
        "extraPlugins": ",".join([
            "image2",
            "justify",
            "colorbutton",
            "font",
            "widget",
            "lineutils",
        ]),
        "removePlugins": "image",
        "image2_alignClasses": ["img-left", "img-center", "img-right"],
        "image2_captionedClass": "image-captioned",
        "image2_disableResizer": False,
        "stylesSet": "custom_styles:/static/core/js/ckeditor/styles.js",
        "contentsCss": ["/static/core/css/global_core.css"],
        "image_prefillDimensions": False,
        "allowedContent": True,
    },

    "user_minimal": {
        "toolbar": [
            ["Bold", "Italic", "Underline", "Strike", "RemoveFormat"],
            ["NumberedList", "BulletedList"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock"],
            ["Link", "Unlink"],
        ],
        "height": 200,
        "width": "auto",
        "removePlugins": "uploadimage,uploadfile,image,sourcearea",
    },

    "moloshop": {
        "language": "ru",
        "height": 350,
        "width": "auto",
        "toolbarCanCollapse": True,
        "removePlugins": "exportpdf",
        "extraPlugins": ",".join([
            "uploadimage",
            "image2",
            "justify",
            "colorbutton",
            "font",
            "tableresize",
        ]),
        "toolbar": "Custom",
        "toolbar_Custom": [
            {"name": "clipboard", "items": ["Undo", "Redo"]},
            {"name": "basicstyles", "items": ["Bold", "Italic", "Underline", "Strike", "RemoveFormat"]},
            {"name": "paragraph", "items": ["NumberedList", "BulletedList", "-", "Outdent", "Indent", "-", "Blockquote"]},
            {"name": "align", "items": ["JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock"]},
            {"name": "links", "items": ["Link", "Unlink"]},
            {"name": "insert", "items": ["Image", "Table", "HorizontalRule"]},
            {"name": "styles", "items": ["Format", "Font", "FontSize"]},
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "document", "items": ["Source"]},
        ],
        "allowedContent": True,
        "disallowedContent": "script; *[on*]",
        "image2_alignClasses": ["img-left", "img-center", "img-right"],
        "image2_disableResizer": False,
        "removeDialogTabs": "image:advanced;link:advanced",
        "contentsCss": ["/static/core/css/global_core.css"],
        "format_tags": "p;h2;h3;h4;pre",
        "tabSpaces": 4,
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# # -----------------------------------
# # Login / Logout redirects
# # -----------------------------------
#
# # URL для @login_required, если пользователь не аутентифицирован
# LOGIN_URL = '/users/login/'
#
# # Куда редиректить после успешного логина
# LOGIN_REDIRECT_URL = '/users/profile/edit/'
#
# # Куда редиректить после логаута
# LOGOUT_REDIRECT_URL = '/'
