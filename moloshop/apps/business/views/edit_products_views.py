
# apps/business/views/edit_products_views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.business.forms.edit_products_item import get_item_form
from apps.business.models import Business

@login_required
def goods_edit(request, business_slug, item_slug):
    from apps.business.models import Goods
    return _item_edit(request, business_slug, item_slug, Goods)

@login_required
def service_edit(request, business_slug, item_slug):
    from apps.business.models import Service
    return _item_edit(request, business_slug, item_slug, Service)

def _item_edit(request, business_slug, item_slug, model_class):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    if item_slug == "new":
        return redirect("business:goods_create" if model_class.__name__ == "Goods" else "business:service_create", business_slug=business.slug)

    item = get_object_or_404(model_class, slug=item_slug, business=business)
    ItemForm = get_item_form(model_class)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("business:business_edit", slug=business.slug)
    else:
        form = ItemForm(instance=item)

    return render(
        request,
        "business/products/products_edit.html",
        {"form": form, "business": business}
    )
