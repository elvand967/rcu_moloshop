
# apps/business/admin/__init__.py


"""
Автоматический импорт всех модулей админки внутри apps/business/admin/.
Чтобы не забывать явно подключать каждый файл.
===old===
from .business_admin import *
from .product_admin import *
from .landing_admin import *
from .order_admin import *
from .promotion_admin import *
"""

import importlib
import pkgutil
from django.conf import settings

# Получаем путь пакета
package_name = __name__  # "apps.core.admin"
package = importlib.import_module(package_name)

# Автоматически импортируем все .py файлы, кроме __init__.py
for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
    if not is_pkg:  # только файлы, не подпакеты
        importlib.import_module(f"{package_name}.{module_name}")


# from django.contrib import admin
#
# from .business import BusinessAdmin
# from .landing import LandingAdmin
# from .goods import GoodsAdmin
# from .services import ServiceAdmin
#
# from apps.business.models.business import Business
# from apps.business.models.landing import Landing
# from apps.business.models.products import Goods, Service
#
#
# # Единая регистрация всех админов
# admin.site.register(Business, BusinessAdmin)
# admin.site.register(Landing, LandingAdmin)
# admin.site.register(Goods, GoodsAdmin)
# admin.site.register(Service, ServiceAdmin)
