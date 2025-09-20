
# ../apps/main/models/__init__.py
'''
Импортируйте сюда все модели, которые собираетесь использовать снаружи/
Это позволит в коде (например, в других приложениях) писать:
'from apps.main.models import GalleryServices'
Если у вас будут и другие классы или модули, например
abstract.NamedSlugModel,
или
moloshop/apps/core/models/other_models.py,
то можно расширить __init__.py:

from .gallery import GalleryServices
'''

# from .gallery import GalleryServices