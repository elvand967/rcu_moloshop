
# apps/business/views/business_options.py


from django.shortcuts import render, get_object_or_404, redirect
from apps.business.forms.business_form import BusinessForm
from django.db.models import Prefetch

from apps.business.forms.productss_form import ProductForm, ServiceForm
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


# =============================
# CRUD для Бизнеса
# =============================
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
            messages.success(request, "Изменения сохранены.")
            return redirect("business:business_edit", slug=business.slug)
    else:
        form = BusinessForm(instance=business)

    return render(request, "business/showcase/business_edit.html", {
        "form": form,
        "business": business,
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


# =============================
# CRUD для Товаров
# =============================
@login_required
def goods_create(request, business_slug):
    '''
    Используем промежуточный шаблон с вводом названия товара.
    Он создаст новую сущность модели с слагом и привязкой к бизнесу.
    Далее в форме редактирования товара уже будут все необходимые параметры
    для работы блока формы ajax-загрузки изображения.
    '''

    business = get_object_or_404(Business, slug=business_slug, owner=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        if not title:
            messages.error(request, "Введите название товара")
        else:
            product = Product.objects.create(
                business=business,
                title=title,
            )
            messages.success(request, f"Товар «{product.title}» создан. Теперь добавьте описание и фото.")
            return redirect("business:goods_edit", business_slug=business.slug, slug=product.slug)

    return render(request, "business/products/product_new.html", {
        "business": business,
    })


@login_required
def goods_edit(request, business_slug, slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    product = get_object_or_404(Product, slug=slug, business=business)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Товар «{product.title}» обновлён.")
            return redirect("business:business_edit", slug=business.slug)
    else:
        form = ProductForm(instance=product)

    return render(request, "business/products/product_form.html", {
        "business": business,
        "form": form,
        "product": product,
    })


@login_required
def goods_delete(request, business_slug, slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    product = get_object_or_404(Product, slug=slug, business=business)
    if request.method == "POST":
        product.delete()
        messages.success(request, f"Товар «{product.title}» удалён.")
    return redirect("business:business_edit", slug=business.slug)


# =============================
# CRUD для Услуг
# =============================
@login_required
def service_create(request, business_slug):
    '''
    Используем промежуточный шаблон с вводом названия товара.
    Он создаст новую сущность модели с слагом и привязкой к бизнесу.
    Далее в форме редактирования товара уже будут все необходимые параметры
    для работы блока формы ajax-загрузки изображения.
    '''

    business = get_object_or_404(Business, slug=business_slug, owner=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        if not title:
            messages.error(request, "Введите название услуги")
        else:
            service = Service.objects.create(
                business=business,
                title=title,
            )
            messages.success(request, f"Услуга «{service.title}» создана. Теперь добавьте описание и фото.")
            return redirect("business:service_edit", business_slug=business.slug, slug=service.slug)

    return render(request, "business/products/service_new.html", {
        "business": business,
    })


@login_required
def service_edit(request, business_slug, slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    service = get_object_or_404(Service, slug=slug, business=business)

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f"Услуга «{service.title}» обновлена.")
            return redirect("business:business_edit", slug=business.slug)
    else:
        form = ServiceForm(instance=service)

    return render(request, "business/products/service_form.html", {
        "business": business,
        "form": form,
        "service": service,
    })


@login_required
def service_delete(request, business_slug, slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    service = get_object_or_404(Service, slug=slug, business=business)
    if request.method == "POST":
        service.delete()
        messages.success(request, f"Услуга «{service.title}» удалена.")
    return redirect("business:business_edit", slug=business.slug)


__all__ = [
    "business_list", "business_detail",
    "business_create", "business_edit",
    "business_delete",
    "goods_create", "goods_edit", "goods_delete",
    "service_create", "service_edit", "service_delete",
]


