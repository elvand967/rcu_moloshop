
# apps/users/urls.py

from django.urls import path
from .views.log import *
from .views.profiles import UserProfileEditView, UploadAvatarView, ResetAvatarView


app_name = "users"

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("profile/edit/", UserProfileEditView.as_view(), name="profile_edit"),
    path("profile/upload-avatar/", UploadAvatarView.as_view(), name="upload_avatar"),
    path("profile/reset-avatar/", ResetAvatarView.as_view(), name="reset_avatar"),
]
