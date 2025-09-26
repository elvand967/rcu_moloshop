
# apps/business/views/logo_upload.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.business.models import Business
from apps.business.forms.logo_form import BusinessLogoForm
from apps.core.utils.loading_media import process_business_logo


@login_required
def upload_logo(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)

    if request.method == "POST":
        form = BusinessLogoForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["logo"]

            # вызываем утилиту
            logo_path, favicon_path = process_business_logo(file, business.slug)

            # сохраняем пути в модель
            business.logo = logo_path
            business.favicon = favicon_path
            business.save(update_fields=["logo", "favicon"])

            return redirect("business:business_edit", slug=business.slug)
    else:
        form = BusinessLogoForm()

    return render(
        request,
        "business/logo_upload.html",
        {"form": form, "business": business}
    )
