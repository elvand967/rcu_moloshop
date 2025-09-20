
# apps/business/urls.py

from django.urls import path

from apps.business.views import edit_products_views
from apps.business.models import Goods, Service
from .views.business_list import user_business_list

app_name = "business"

urlpatterns = [

    # Список/карточки бизнесов   "business/showcase/user_business_list.html"
    path("businesses/", user_business_list, name="user_business_list"),

    # Редактор товаров
    path("<slug:business_slug>/goods/<slug:item_slug>/edit/",
         lambda request, business_slug, item_slug: edit_products_views.item_edit(request, business_slug, item_slug, Goods),
         name="goods_edit"),

    # Редактор услуг
    path("<slug:business_slug>/services/<slug:item_slug>/edit/",
         lambda request, business_slug, item_slug: edit_products_views.item_edit(request, business_slug, item_slug, Service),
         name="service_edit"),
]