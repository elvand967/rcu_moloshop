
# apps/business/views/business_options.py


from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.business.forms.business_form import BusinessForm
from django.db.models import Prefetch

from apps.business.forms.productss_form import ProductForm, ServiceForm
from apps.business.models import Business, Product, Service, Media
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import JsonResponse

from apps.users.models import ProfileMenuCategory

'''
Декоратор login_required в Django используется во вьюшках для 
ограничения доступа к этим вьюшкам только аутентифицированным пользователям. 
Если пользователь не вошёл в систему (не авторизован), 
то при обращении к такой защищённой вьюшке происходит автоматический редирект на страницу входа (логина). 
После успешного входа пользователя перенаправляют обратно к запрошенной странице.

Использование декоратора login_required в данном коде корректно и оправдано, 
даже если все представления доступны только из личного кабинета авторизованных пользователей.
'''

# @login_required
# def business_list(request):
#     """
#     Отображает список бизнесов текущего пользователя вместе с товарами, услугами и медиа.
#     """
#
#     products = Product.objects.prefetch_related("media")
#     services = Service.objects.prefetch_related("media")
#
#     businesses = (
#         Business.objects.filter(owner=request.user)
#         .order_by("order", "title")
#         .prefetch_related(
#             Prefetch("products", queryset=products),
#             Prefetch("services", queryset=services),
#         )
#     )
#
#     return render(
#         request,
#         "business/showcase/business_list.html",
#         {"businesses": businesses},
#     )

@login_required
# Декоратор, который гарантирует, что доступ к функции будет только у аутентифицированных пользователей.
# Если пользователь не вошёл в систему, его перенаправляют на страницу входа.
def business_list(request):
    # Определение функции представления business_list, которая обрабатывает HTTP-запрос.

    """
    Отображает список бизнесов текущего пользователя вместе с товарами, услугами и медиа.
    """

    products = Product.objects.prefetch_related("media")
    # Запрос к базе данных для получения всех товаров с предварительной загрузкой связанных объектов 'media' (медиафайлов) для оптимизации.

    services = Service.objects.prefetch_related("media")
    # Аналогичный запрос для услуг, тоже с предварительной загрузкой связанных медиафайлов.

    businesses = (
        Business.objects.filter(owner=request.user)
        # Фильтруем объекты бизнесов по владельцу - текущему аутентифицированному пользователю.

        .order_by("order", "title")
        # Сортируем бизнесы сначала по полю 'order', затем по 'title' в алфавитном порядке.

        .prefetch_related(
            Prefetch("products", queryset=products),
            Prefetch("services", queryset=services),
        )
        # Оптимизация запросов: для каждого бизнеса заранее подгружаем связанные товары и услуги
        # используя ранее определённые запросы с медиа.
    )

    return render(
        request,
        "business/showcase/business_list.html",
        {"businesses": businesses},
    )
    # Рендерит HTML-шаблон "business_list.html" и передает в контекст переменную 'businesses' —
    # queryset бизнесов, чтобы отобразить их на странице для пользователя.


# =============================
# CRUD для Бизнеса
# =============================
@login_required
def business_create(request):
    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()

            # Ищем глобальный корень "Мои бизнесы"
            root_menu = get_object_or_404(ProfileMenuCategory, user__isnull=True, name="Мои бизнесы", parent=None)

            # Создаём бизнес как дочерний к этому глобальному корню
            business_menu = ProfileMenuCategory.objects.create(
                user=request.user,
                name=business.title,
                url='business:business_edit',
                url_params={'business_slug': business.slug},
                order=0,
                parent=root_menu,
            )

            # Создаём подпункты 3-го уровня
            ProfileMenuCategory.objects.create(
                user=request.user,
                name='Адрес',
                url='business:business_address_edit',
                url_params={'business_slug': business.slug},
                order=1,
                parent=business_menu,
            )
            ProfileMenuCategory.objects.create(
                user=request.user,
                name='Контакты',
                url='business:business_contacts_edit',
                url_params={'business_slug': business.slug},
                order=2,
                parent=business_menu,
            )
            ProfileMenuCategory.objects.create(
                user=request.user,
                name='Товары',
                url='business:business_products_list',
                url_params={'business_slug': business.slug},
                order=3,
                parent=business_menu,
            )
            ProfileMenuCategory.objects.create(
                user=request.user,
                name='Услуги',
                url='business:business_services_list',
                url_params={'business_slug': business.slug},
                order=4,
                parent=business_menu,
            )

            messages.success(request, "Бизнес успешно создан и добавлен в меню.")
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
        # Удаляем бизнес
        business.delete()

        # Ищем пункт меню 2-го уровня с именем бизнеса и пользователем
        menu_item = ProfileMenuCategory.objects.filter(
            user=request.user,
            name=business.title,
            parent__isnull=False  # 2-й уровень (дочерний к корню)
        ).first()

        if menu_item:
            # Удаляем пункт меню и все его потомки из дерева
            menu_item.delete()

        messages.success(request, f"Бизнес '{business.title}' и его меню успешно удалены.")
        return redirect("business:business_list")

    # GET-запрос: показать подтверждение удаления (можно сделать модальное окно на фронтенде)
    messages.warning(request, f"Подтвердите удаление бизнеса '{business.title}' через POST-запрос.")
    return redirect("business:business_list")


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

    # Добавляем галерею в context
    gallery = product.gallery.all()

    return render(request, "business/products/product_form.html", {
        "business": business,
        "form": form,
        "product": product,
        "gallery": gallery,
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
    # Получаем бизнес по slug, фильтруем по владельцу (аутентифицированному пользователю)
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    # Получаем услугу по slug и бизнесу
    service = get_object_or_404(Service, slug=slug, business=business)

    if request.method == "POST":
        # Если запрос POST - создаём форму с данными из запроса и файлами, с привязкой к экземпляру услуги
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            # Если форма корректна, сохраняем объект
            form.save()
            # Добавляем сообщение об успехе
            messages.success(request, f"Услуга «{service.title}» обновлена.")
            # Перенаправляем на страницу редактирования бизнеса
            return redirect("business:business_edit", slug=business.slug)
    else:
        # Если метод запроса не POST, создаём форму с данными из существующего объекта
        form = ServiceForm(instance=service)

    # Получаем связанные медиа-объекты галереи услуги
    gallery = service.gallery.all()

    # Рендерим шаблон, передавая контекст с бизнесом, формой, услугой и галереей
    return render(request, "business/products/service_form.html", {
        "business": business,
        "form": form,
        "service": service,
        "gallery": gallery,
    })


@login_required
def service_delete(request, business_slug, slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    service = get_object_or_404(Service, slug=slug, business=business)
    if request.method == "POST":
        service.delete()
        messages.success(request, f"Услуга «{service.title}» удалена.")
    return redirect("business:business_edit", slug=business.slug)


@login_required
def delete_gallery_image(request, business_slug, model_type, model_slug, media_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    if model_type == "product":
        obj = get_object_or_404(Product, slug=model_slug, business=business)
    elif model_type == "service":
        obj = get_object_or_404(Service, slug=model_slug, business=business)
    else:
        return JsonResponse({"error": "Invalid model type"}, status=400)

    media = obj.gallery.filter(id=media_id).first()
    if not media:
        return JsonResponse({"error": "Media not found"}, status=404)

    if media.file:
        media.file.delete(save=False)
    media.delete()

    return JsonResponse({"success": True})



__all__ = [
    "business_list", "business_detail",
    "business_create", "business_edit",
    "business_delete",
    "goods_create", "goods_edit", "goods_delete",
    "service_create", "service_edit", "service_delete",
    "delete_gallery_image",
]


