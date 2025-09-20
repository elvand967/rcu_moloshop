
# ../apps/core/models/__init__.py
'''
Импортируйте сюда все абстрактные модели, которые собираетесь использовать снаружи/
Это позволит в коде (например, в других приложениях) писать:
'from apps.core.models import UUIDModel'
Если у вас будут и другие классы или модули, например
abstract.NamedSlugModel,
или
moloshop/apps/core/models/other_models.py,
то можно расширить __init__.py:

from .abstract import UUIDModel, NamedSlugModel
from .other_models import SomeOtherModel
'''
from .abstract import UUIDModel, NamedSlugModel, SlugNamespaceModel
from .seo import StopWord, SEOReplacement
from .footer_menu import FooterMenuCategory
from .core_documents import ContractsInstructions