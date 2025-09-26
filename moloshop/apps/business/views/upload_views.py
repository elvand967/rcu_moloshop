
# +apps/business/views/upload_views.py

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from apps.business.models import Business
from apps.core.utils.loading_media import UPLOAD_CONFIG, process_image
from apps.business.forms.image_upload_form import ImageUploadForm

'''
Получаем бизнес по слагу и проверяем владельца.
Проверяем, что тип изображения есть в конфиге.
Инициализируем форму с нужным именем поля.
При POST валидируем, обрабатываем и сохраняем изображение.
При GET отображаем пустую форму.
После успешной загрузки редиректим на редактирование бизнеса.
'''

@login_required
def upload_image(request, business_slug, image_type):
    """
    Вью для универсальной загрузки изображений бизнес-объекта по типу.
    """
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)

    config = UPLOAD_CONFIG.get(image_type)
    if not config:
        return redirect("business:business_edit", slug=business.slug)

    field_name = config["field"]

    if request.method == "POST":
        form = ImageUploadForm(field_name, request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data[field_name]
            process_image(file, business, image_type)
            business.save(update_fields=[config.get("target_field", field_name)])
            return redirect("business:business_edit", slug=business.slug)
    else:
        form = ImageUploadForm(field_name)

    return render(request, "business/img_upload.html", {
        "form": form,
        "business": business,
        "image_type": image_type,
        "field_name": field_name,
    })