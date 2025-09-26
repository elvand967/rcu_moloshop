
# apps/business/urls.py

from django.urls import path
from apps.business.views import business_list, business_create, business_edit, business_detail, business_delete, \
    upload_views, ajax_upload
# from apps.business.views import edit_products_views, products_create
from apps.business.views.ajax_upload import upload_logo, upload_favicon, delete_logo, delete_favicon
from apps.business.views.upload_views import upload_image

app_name = "business"

urlpatterns = [
    path("businesses/", business_list, name="business_list"),
    path("create/", business_create, name="business_create"),
    path("<slug:slug>/edit/", business_edit, name="business_edit"),
    path("<slug:slug>/", business_detail, name="business_detail"),
    path("<slug:slug>/delete/", business_delete, name="business_delete"),

    # # Создание товара / услуги
    # path("<slug:business_slug>/goods/create/", products_create.goods_create, name="goods_create"),
    # path("<slug:business_slug>/services/create/", products_create.service_create, name="service_create"),
    #
    # # Редактирование товара / услуги
    # path("<slug:business_slug>/goods/<slug:item_slug>/edit/", edit_products_views.goods_edit, name="goods_edit"),
    # path("<slug:business_slug>/services/<slug:item_slug>/edit/", edit_products_views.service_edit, name="service_edit"),

    # Загрузка/удаление логотипа/фавикона, с AJAX запросом
    path('<slug:business_slug>/edit/upload_logo/', upload_logo, name='upload_logo'),
    path('<slug:business_slug>/edit/upload_favicon/', upload_favicon, name='upload_favicon'),
    path("<slug:business_slug>/delete_logo/", delete_logo, name="delete_logo"),
    path("<slug:business_slug>/delete_favicon/", delete_favicon, name="delete_favicon"),

]
