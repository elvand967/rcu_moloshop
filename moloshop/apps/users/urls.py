
# apps/users/urls.py

from django.urls import path
from .views.log import *

app_name = "users"

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
