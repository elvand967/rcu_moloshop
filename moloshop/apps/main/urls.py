
# ..p/apps/main/urls.py

from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home_view, name='includes'),
    path('test/', views.home_view, name='test'),
]
