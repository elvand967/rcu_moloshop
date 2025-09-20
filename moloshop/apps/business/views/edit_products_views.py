
# apps/business/views/edit_products_views.py

from django.shortcuts import get_object_or_404, render, redirect
from apps.business.models import Goods, Service, Business
from apps.business.forms.edit_products_item import get_item_form


def item_edit(request, business_slug, item_slug, model):
    business = get_object_or_404(Business, slug=business_slug)
    obj = get_object_or_404(model, business=business, slug=item_slug)

    ItemForm = get_item_form(model)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("business:user_business_list")
    else:
        form = ItemForm(instance=obj)

    # передаём verbose_name в шаблон
    verbose_name = model._meta.verbose_name

    return render(
        request,
        "business/products/edit_products.html",
        {
            "form": form,
            "object": obj,
            "business": business,
            "verbose_name": verbose_name,
        },
    )