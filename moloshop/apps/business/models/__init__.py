
# apps/business/models/__init__.py
'''
Импортируйте сюда все модели, которые собираетесь использовать снаружи/
Это позволит в коде (например, в других приложениях) писать:
'from apps.business.models import Business'
Если у вас будут и другие классы или модули, например:
moloshop/apps/business/models/other_models.py,
то можно расширить __init__.py:
from .business import Business
from .landing import Landing
'''

from .business import *
from .business_products import *
from .staff import *



# from .business import Business, ContactInfo, Messenger
# from .business_products import Category, Product, Service
# from .staff import Staff
# from .landing import Landing, Section, SectionImage
# from .order import Order
# from .promotion import Promotion