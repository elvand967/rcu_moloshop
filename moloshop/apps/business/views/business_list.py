# apps/users/views/business_list.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.business.models.business import Business

@login_required
def user_business_list(request):
    """
    Отображает список бизнесов текущего пользователя вместе с товарами и услугами.
    """
    businesses = (
        Business.objects.filter(owner=request.user)
        .order_by("order", "title")
        .prefetch_related("goods", "services")  # <= меняем!
    )
    return render(
        request,
        "business/showcase/user_business_list.html",
        {"businesses": businesses},
    )
