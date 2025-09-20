# apps/users/forms/profile_menu_category_form.py

from django import forms
from apps.users.models.menu import ProfileMenuCategory
from apps.core.utils.url_registry import get_all_named_urls


class ProfileMenuCategoryForm(forms.ModelForm):
    class Meta:
        model = ProfileMenuCategory
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Подставляем choices из get_all_named_urls
        self.fields['url'].widget = forms.Select(choices=[('', '---')] + get_all_named_urls())

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        external_url = cleaned_data.get("external_url")

        # Запрещаем одновременный ввод
        if url and external_url:
            raise forms.ValidationError(
                "Нельзя одновременно задать Django-URL и внешнюю ссылку."
            )

        # Запрещаем пустоту обоих
        if not url and not external_url:
            raise forms.ValidationError(
                "Нужно указать либо Django-URL, либо внешнюю ссылку."
            )

        return cleaned_data
