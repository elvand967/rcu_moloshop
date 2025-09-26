
# apps/business/views/business_options.py


from django.shortcuts import render, get_object_or_404, redirect
from apps.business.forms.business_form import BusinessForm
from django.db.models import Prefetch
from apps.business.models import Business, Product, Service, Media
from django.contrib.auth.decorators import login_required
from django.contrib import messages

'''
Декоратор login_required в Django используется во вьюшках для 
ограничения доступа к этим вьюшкам только аутентифицированным пользователям. 
Если пользователь не вошёл в систему (не авторизован), 
то при обращении к такой защищённой вьюшке происходит автоматический редирект на страницу входа (логина). 
После успешного входа пользователя перенаправляют обратно к запрошенной странице.

Использование декоратора login_required в данном коде корректно и оправдано, 
даже если все представления доступны только из личного кабинета авторизованных пользователей.
'''

@login_required
def business_list(request):
    """
    Отображает список бизнесов текущего пользователя вместе с товарами, услугами и медиа.
    """

    products = Product.objects.prefetch_related("media")
    services = Service.objects.prefetch_related("media")

    businesses = (
        Business.objects.filter(owner=request.user)
        .order_by("order", "title")
        .prefetch_related(
            Prefetch("products", queryset=products),
            Prefetch("services", queryset=services),
        )
    )

    return render(
        request,
        "business/showcase/business_list.html",
        {"businesses": businesses},
    )


@login_required
def business_create(request):
    """
    Создание нового бизнеса
    """
    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            return redirect("business:business_edit", business.slug)
    else:
        form = BusinessForm()
    return render(request, "business/showcase/business_create.html", {"form": form})


@login_required
def business_edit(request, slug):
    """
    Редактирование существующего бизнеса
    """
    business = get_object_or_404(Business, slug=slug, owner=request.user)

    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect("business:business_edit", slug=business.slug)
    else:
        form = BusinessForm(instance=business)

    # Важно: передаем 'business' в контекст
    return render(request, "business/showcase/business_edit.html", {
        "form": form,
        "business": business
    })


@login_required
def business_detail(request, slug):
    """
    Просмотр карточки бизнеса
    """
    business = get_object_or_404(Business, slug=slug)
    return render(request, "business/showcase/business_detail.html", {"business": business})


@login_required
def business_delete(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)

    if request.method == "POST":
        business.delete()
        messages.success(request, f"Бизнес '{business.title}' удалён.")
        return redirect("business:business_list")

    # GET-запрос: показать подтверждение удаления (можно сделать модальное окно на фронтенде)
    messages.warning(request, f"Подтвердите удаление бизнеса '{business.title}' через POST-запрос.")
    return redirect("business:business_list")


__all__ = ["business_list", "business_create", "business_edit", "business_detail", "business_delete"]

