
# ../apps/core/forms/footer_menu.py

from django import forms
from apps.core.models.footer_menu import FooterMenuCategory
from apps.core.utils.url_registry import get_all_named_urls


class FooterMenuCategoryForm(forms.ModelForm):
    url = forms.ChoiceField(
        required=False,
        choices=[],
        help_text="Выберите внутренний маршрут (если используется)"
    )

    class Meta:
        model = FooterMenuCategory
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # загружаем список роутов (можно ограничить по приложениям: app_names=None или app_names=['core', 'main'])
        self.fields["url"].choices = [("", "—")] + get_all_named_urls(app_names=['core', 'main'])

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        external_url = cleaned_data.get("external_url")

        # проверяем, чтобы не было двух ссылок одновременно
        if url and external_url:
            raise forms.ValidationError(
                "Нельзя указывать одновременно внутреннюю и внешнюю ссылку. "
                "Выберите только один вариант."
            )

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get("name")
        icon = self.cleaned_data.get("icon")
        if not name and icon:
            # если нет названия, но есть иконка → подставляем имя файла
            return icon.name.rsplit(".", 1)[0]
        return name


