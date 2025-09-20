
# apps/users/admin/__init__.py

"""
Автоматический импорт всех модулей админки внутри apps/users/admin/.
Чтобы не забывать явно подключать каждый файл (core_documents.py, core_settings.py и др.).
---
old-было:
# Импортируем регистрацию, чтобы Django увидел админки
from .user_admin import CustomUserAdmin
from .profile_admin import UserProfileAdmin
from .social_admin import UserSocialLinkAdmin
"""

import importlib
import pkgutil

# Получаем путь пакета
package_name = __name__  # "apps.users.admin"
package = importlib.import_module(package_name)

# Автоматически импортируем все .py файлы, кроме __init__.py
for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
    if not is_pkg:
        importlib.import_module(f"{package_name}.{module_name}")