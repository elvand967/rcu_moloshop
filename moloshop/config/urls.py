
# ../config/urls.py


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls', namespace='main')),
    path('core/', include('apps.core.urls')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('business/', include('apps.business.urls', namespace='business')),
    path('ckeditor/', include('ckeditor_uploader.urls')), # маршруты аплоада
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
