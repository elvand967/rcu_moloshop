
# apps/business/views/products_create.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.business.models import Business
from apps.business.forms.edit_products_item import get_item_form
from apps.business.models import Goods, Service

@login_required
def goods_create(request, business_slug):
    return _product_create(request, business_slug, Goods)

@login_required
def service_create(request, business_slug):
    return _product_create(request, business_slug, Service)

def _product_create(request, business_slug, model_class):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    ItemForm = get_item_form(model_class)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.business = business
            instance.save()
            return redirect(
                "business:goods_edit" if model_class == Goods else "business:service_edit",
                business_slug=business.slug,
                item_slug=instance.slug
            )
    else:
        form = ItemForm()

    return render(
        request,
        "business/products/products_create.html",
        {"form": form, "business": business, "is_goods": model_class == Goods}
    )
