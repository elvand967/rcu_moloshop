
# apps/business/views/business_options.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from apps.business.forms.business_form import BusinessForm
from django.db.models import Prefetch
from apps.business.forms.productss_form import GoodsForm, ServiceForm, ServiceTitleForm, GoodsTitleForm
from apps.business.models import Business, Goods, Service, Media
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from apps.users.models import ProfileMenuCategory
from django.utils.http import urlencode

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
'''
Декоратор login_required в Django используется во вьюшках для 
ограничения доступа к этим вьюшкам только аутентифицированным пользователям. 
Если пользователь не вошёл в систему (не авторизован), 
то при обращении к такой защищённой вьюшке происходит автоматический редирект на страницу входа (логина). 
После успешного входа пользователя перенаправляют обратно к запрошенной странице.

Использование декоратора login_required в данном коде корректно и оправдано, 
даже если все представления доступны только из личного кабинета авторизованных пользователей.
'''

# =============================
# CRUD для Бизнеса
# =============================
@login_required
# Декоратор, который гарантирует, что доступ к функции будет только у аутентифицированных пользователей.
# Если пользователь не вошёл в систему, его перенаправляют на страницу входа.
def business_list(request):
    # Определение функции представления business_list, которая обрабатывает HTTP-запрос.

    """
    Отображает список бизнесов текущего пользователя вместе с товарами, услугами и медиа.
    """

    goodss = Goods.objects.prefetch_related("media")
    # Запрос к базе данных для получения всех товаров с предварительной загрузкой связанных объектов 'media' (медиафайлов) для оптимизации.

    services = Service.objects.prefetch_related("media")
    # Аналогичный запрос для услуг, тоже с предварительной загрузкой связанных медиафайлов.

    businesses = (
        Business.objects.filter(owner=request.user)
        # Фильтруем объекты бизнесов по владельцу - текущему аутентифицированному пользователю.

        .order_by("order", "title")
        # Сортируем бизнесы сначала по полю 'order', затем по 'title' в алфавитном порядке.

        .prefetch_related(
            Prefetch("goodss", queryset=goodss),
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
                url='business:goods_list',
                url_params={'business_slug': business.slug},
                order=3,
                parent=business_menu,
            )
            ProfileMenuCategory.objects.create(
                user=request.user,
                name='Услуги',
                url='business:service_list',
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
        form = GoodsTitleForm(request.POST)
        if form.is_valid():
            goods = form.save(commit=False)
            goods.business = business
            goods.save()
            messages.success(request, f"Товар «{goods.title}» создана.")
            params = urlencode({"active_goods_id": goods.id})
            return redirect(f"{reverse('business:goods_list', kwargs={'business_slug': business.slug})}?{params}")
    else:
        form = GoodsTitleForm()
    return render(request, "business/products/goods_new.html", {"form": form, "business": business})


@login_required
def goods_list(request, business_slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)

    goodss_qs = Goods.objects.filter(business=business).order_by("-created_at")

    # --- Пагинация ---
    paginator = Paginator(goodss_qs, 5)  # по 5 услуг на страницу
    page_number = request.GET.get("page")
    try:
        goodss_page = paginator.page(page_number)
    except PageNotAnInteger:
        goodss_page = paginator.page(1)
    except EmptyPage:
        goodss_page = paginator.page(paginator.num_pages)

    # Подгружаем галерею для всех товаров, попавших на текущую страницу
    media_qs = Media.objects.filter(
        content_type__model='goods',
        object_id__in=goodss_page.object_list.values_list('id', flat=True)
    )

    # Словарь goods.id -> список Media
    gallery_dict = {}
    for media in media_qs:
        gallery_dict.setdefault(media.object_id, []).append(media)

    active_goods_id = request.GET.get("active_goods_id")
    try:
        active_goods_id = int(active_goods_id)
    except (TypeError, ValueError):
        active_goods_id = None

    if request.method == "POST":
        if "goods_id" in request.POST:
            goods_id = request.POST.get("goods_id")
            goods = get_object_or_404(Goods, pk=goods_id, business=business)
            form = GoodsForm(request.POST, instance=goods)
            if form.is_valid():
                form.save()
                messages.success(request, "Изменения сохранены.")
                return redirect("business:goods_list", business_slug=business.slug)
        else:
            form = GoodsForm(request.POST)
            if form.is_valid():
                new_goods = form.save(commit=False)
                new_goods.business = business
                new_goods.save()
                messages.success(request, "Товар добавлен.")
                return redirect("business:goods_list", business_slug=business.slug)

    goods_forms = {s.id: GoodsForm(instance=s) for s in goodss_page}
    new_goods_form = GoodsForm()

    return render(request, "business/products/goods_list.html", {
        "business": business,
        "goodss": goodss_page,  # заменили queryset на страницу
        "goods_forms": goods_forms,
        "new_goods_form": new_goods_form,
        "active_goods_id": active_goods_id,
        "gallery_dict": gallery_dict,
        "paginator": paginator,
    })


@login_required
def goods_edit(request, business_slug, slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    goods = get_object_or_404(Goods, slug=slug, business=business)  # Goods

    if request.method == "POST":
        form = GoodsForm(request.POST, request.FILES, instance=goods)  # GoodsForm
        if form.is_valid():
            form.save()
            messages.success(request, f"Товар «{goods.title}» обновлён.")
            return redirect("business:business_edit", slug=business.slug)
    else:
        form = GoodsForm(instance=goods)

    gallery = goods.gallery.all()

    return render(request, "business/products/goods_form.html", {
        "business": business,
        "form": form,
        "goods": goods,
        "gallery": gallery,
    })


@login_required
def goods_delete(request, business_slug, slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    product = get_object_or_404(Goods, slug=slug, business=business)  # Goods
    if request.method == "POST":
        product.delete()
        messages.success(request, f"Товар «{product.title}» удалён.")
    return redirect("business:business_edit", slug=business.slug)


# =============================
# CRUD для Услуг
# =============================
@login_required
def service_create(request, business_slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    if request.method == "POST":
        form = ServiceTitleForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.business = business
            service.save()
            messages.success(request, f"Услуга «{service.title}» создана.")
            params = urlencode({"active_service_id": service.id})
            return redirect(f"{reverse('business:service_list', kwargs={'business_slug': business.slug})}?{params}")
    else:
        form = ServiceTitleForm()
    return render(request, "business/products/service_new.html", {"form": form, "business": business})


@login_required
def service_list(request, business_slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)

    services_qs = Service.objects.filter(business=business).order_by("-created_at")

    # --- Пагинация ---
    paginator = Paginator(services_qs, 5)  # по 5 услуг на страницу
    page_number = request.GET.get("page")
    try:
        services_page = paginator.page(page_number)
    except PageNotAnInteger:
        services_page = paginator.page(1)
    except EmptyPage:
        services_page = paginator.page(paginator.num_pages)

    # Подгружаем галерею для всех услуг, попавших на текущую страницу
    media_qs = Media.objects.filter(
        content_type__model='service',
        object_id__in=services_page.object_list.values_list('id', flat=True)
    )

    # Словарь service.id -> список Media
    gallery_dict = {}
    for media in media_qs:
        gallery_dict.setdefault(media.object_id, []).append(media)

    active_service_id = request.GET.get("active_service_id")
    try:
        active_service_id = int(active_service_id)
    except (TypeError, ValueError):
        active_service_id = None

    if request.method == "POST":
        if "service_id" in request.POST:
            service_id = request.POST.get("service_id")
            service = get_object_or_404(Service, pk=service_id, business=business)
            form = ServiceForm(request.POST, instance=service)
            if form.is_valid():
                form.save()
                messages.success(request, "Изменения сохранены.")
                return redirect("business:service_list", business_slug=business.slug)
        else:
            form = ServiceForm(request.POST)
            if form.is_valid():
                new_service = form.save(commit=False)
                new_service.business = business
                new_service.save()
                messages.success(request, "Услуга добавлена.")
                return redirect("business:service_list", business_slug=business.slug)

    service_forms = {s.id: ServiceForm(instance=s) for s in services_page}
    new_service_form = ServiceForm()

    return render(request, "business/products/services_list.html", {
        "business": business,
        "services": services_page,  # заменили queryset на страницу
        "service_forms": service_forms,
        "new_service_form": new_service_form,
        "active_service_id": active_service_id,
        "gallery_dict": gallery_dict,
        "paginator": paginator,
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
        title = service.title
        service.delete()
        messages.success(request, f"Услуга «{title}» успешно удалена.")
    return redirect("business:service_list", business_slug=business.slug)


@login_required
def delete_gallery_image(request, business_slug, model_type, model_slug, media_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    if model_type == "goods":
        obj = get_object_or_404(Goods, slug=model_slug, business=business)
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
    "goods_list", "goods_create", "goods_edit", "goods_delete",
    "service_list", "service_create", "service_edit", "service_delete",
    "delete_gallery_image",
]


