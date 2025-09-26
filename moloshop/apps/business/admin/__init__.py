
# apps/business/admin/__init__.py

"""
Автоматический импорт всех модулей админки внутри apps/business/admin/.
Чтобы не забывать явно подключать каждый файл (business_documents.py, business_settings.py и др.).
---
old - Вместо:
# ../apps/business/admin/__init__.py
"""
from .business import *
from .product import *
from .services import *
from .category import *
from .media import *

# import importlib
# import pkgutil
#
# from django.conf import settings
#
# # Получаем путь пакета
# package_name = __name__  # "apps.core.admin"
# package = importlib.import_module(package_name)
#
# # Автоматически импортируем все .py файлы, кроме __init__.py
# for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
#     if not is_pkg:  # только файлы, не подпакеты
#         importlib.import_module(f"{package_name}.{module_name}")