
# +apps/business/forms/image_upload_form.py

from django import forms

class ImageUploadForm(forms.Form):
    """
    Универсальная форма для загрузки изображения по динамическому полю.
    """
    def __init__(self, field_name="image", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[field_name] = forms.ImageField(
            required=True,
            label=f"Загрузить {field_name}",
            widget=forms.ClearableFileInput(attrs={"class": "form-control"})
        )
