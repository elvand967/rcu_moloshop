
# apps/users/views/profiles.py

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.users.forms.user_profile_form import UserForm, UserProfileForm, AvatarForm
from apps.users.models import UserProfile


class UserProfileEditView(LoginRequiredMixin, View):
    template_name = "users/user_profile_edit.html"

    def get_profile(self, user):
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request):
        profile = self.get_profile(request.user)
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
        avatar_form = AvatarForm()
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "avatar_form": avatar_form,
            "profile": profile,
            "email_not_verified": profile.user_status == 0,
            "email_verified": profile.user_status >= 1,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        profile = self.get_profile(request.user)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        avatar_form = AvatarForm(request.POST, request.FILES)
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "avatar_form": avatar_form,
            "profile": profile,
            "email_not_verified": profile.user_status == 0,
            "email_verified": profile.user_status >= 1,
        }

        if "save_profile" in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Профиль успешно обновлен.")
                return redirect("users:profile_edit")
            messages.error(request, "Исправьте ошибки в форме.")
        elif "upload_avatar" in request.POST and avatar_form.is_valid():
            file = avatar_form.cleaned_data.get("avatar_file")
            if file:
                profile.upload_avatar(file)
                messages.success(request, "Аватарка обновлена.")
            return redirect("users:profile_edit")
        elif "reset_avatar" in request.POST:
            profile.reset_avatar()
            messages.success(request, "Аватарка сброшена на дефолтную.")
            return redirect("users:profile_edit")

        return render(request, self.template_name, context)


class UploadAvatarView(LoginRequiredMixin, View):
    def post(self, request):
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data.get("avatar_file"):
            request.user.profile.upload_avatar(form.cleaned_data["avatar_file"])
            messages.success(request, "Аватарка обновлена.")
        return redirect("users:profile_edit")


class ResetAvatarView(LoginRequiredMixin, View):
    def post(self, request):
        request.user.profile.reset_avatar()
        messages.success(request, "Аватарка сброшена на дефолтную.")
        return redirect("users:profile_edit")