
# apps/business/urls.py

from django.urls import path
from apps.business.views import business_list, business_create, business_edit, business_detail, business_delete

from apps.business.views.ajax_upload import upload_logo, upload_favicon, delete_logo, delete_favicon, \
    upload_product_image, delete_product_image, upload_service_image, delete_service_image, upload_gallery_image
from apps.business.views.business_options import goods_create, goods_edit, service_create, service_edit, goods_delete, \
    service_delete, delete_gallery_image

app_name = "business"

urlpatterns = [
    path("businesses/", business_list, name="business_list"),
    path("create/", business_create, name="business_create"),
    path("<slug:slug>/edit/", business_edit, name="business_edit"),
    path("<slug:slug>/", business_detail, name="business_detail"),
    path("<slug:slug>/delete/", business_delete, name="business_delete"),

    # товары
    path("<slug:business_slug>/goods/create/", goods_create, name="goods_create"),
    path("<slug:business_slug>/goods/<slug:slug>/edit/", goods_edit, name="goods_edit"),
    path("<slug:business_slug>/goods/<slug:slug>/delete/",goods_delete, name="goods_delete"),

    # услуги
    path("<slug:business_slug>/services/create/", service_create, name="service_create"),
    path("<slug:business_slug>/services/<slug:slug>/edit/", service_edit, name="service_edit"),
    path("<slug:business_slug>/services/<slug:slug>/delete/", service_delete, name="service_delete"),

    # Загрузка/удаление логотипа/фавикона, с AJAX запросом
    path('<slug:business_slug>/edit/upload_logo/', upload_logo, name='upload_logo'),
    path('<slug:business_slug>/edit/upload_favicon/', upload_favicon, name='upload_favicon'),
    path("<slug:business_slug>/delete_logo/", delete_logo, name="delete_logo"),
    path("<slug:business_slug>/delete_favicon/", delete_favicon, name="delete_favicon"),

    # Загрузка/удаление обложек карточек товаров/услуг, с AJAX запросом
    path('<slug:business_slug>/products/<slug:product_slug>/upload_image/', upload_product_image, name='upload_product_image'),
    path('<slug:business_slug>/products/<slug:product_slug>/delete_image/', delete_product_image, name='delete_product_image'),

    path('<slug:business_slug>/services/<slug:service_slug>/upload_image/', upload_service_image, name='upload_service_image'),
    path('<slug:business_slug>/services/<slug:service_slug>/delete_image/', delete_service_image, name='delete_service_image'),

    # Загрузка/удаление изображений галереи
    path('<slug:business_slug>/<str:model_type>/<slug:model_slug>/gallery/upload/', upload_gallery_image,
         name='upload_gallery_image'),
    path('<slug:business_slug>/<str:model_type>/<slug:model_slug>/gallery/delete/<uuid:media_id>/', delete_gallery_image,
         name='delete_gallery_image'),


]
