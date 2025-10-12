# apps/business/views/ajax_upload.py


from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from apps.business.models import Business, Goods, Service
from apps.core.utils.loading_media import process_image


@login_required
@require_POST
def upload_logo(request, business_slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    file = request.FILES.get('logo')
    if not file:
        return JsonResponse({'success': False, 'error': 'No file provided'}, status=400)
    process_image(file, business, 'logo')
    business.save(update_fields=['logo'])
    return JsonResponse({'success': True, 'url': business.logo.url})

@login_required
@require_POST
def delete_logo(request, business_slug):
    """
    Удаляет логотип компании и очищает поле модели.
    """
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)

    if business.logo:
        # Удаляем файл из хранилища
        business.logo.delete(save=False)
        # Очищаем поле
        business.logo = None
        business.save(update_fields=['logo'])

    return JsonResponse({'success': True})


@login_required
@require_POST
def upload_favicon(request, business_slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    file = request.FILES.get('favicon')
    if not file:
        return JsonResponse({'success': False, 'error': 'No file provided'}, status=400)
    process_image(file, business, 'favicon')
    business.save(update_fields=['favicon'])
    return JsonResponse({'success': True, 'url': business.favicon.url})

@login_required
@require_POST
def delete_favicon(request, business_slug):
    """
    Удаляет фавикон компании и очищает поле модели.
    """
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)

    if business.favicon:
        # Удаляем файл из хранилища
        business.favicon.delete(save=False)
        # Очищаем поле
        business.favicon = None
        business.save(update_fields=['favicon'])

    return JsonResponse({'success': True})


@login_required
@require_POST
def upload_goods_image(request, business_slug, goods_slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    goods = get_object_or_404(Goods, slug=goods_slug, business=business)
    file = request.FILES.get('image')
    if not file:
        return JsonResponse({'success': False, 'error': 'No file provided'}, status=400)
    process_image(file, goods, 'product_jpg')  # process_image из utils
    goods.save(update_fields=['image'])
    return JsonResponse({'success': True, 'url': goods.image.url})

@login_required
@require_POST
def delete_goods_image(request, business_slug, goods_slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    goods = get_object_or_404(Goods, slug=goods_slug, business=business)
    if goods.image:
        goods.image.delete(save=False)
        goods.image = None
        goods.save(update_fields=['image'])
    return JsonResponse({'success': True})


@login_required
@require_POST
def upload_service_image(request, business_slug, service_slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    service = get_object_or_404(Service, slug=service_slug, business=business)
    file = request.FILES.get('image')
    if not file:
        return JsonResponse({'success': False, 'error': 'No file provided'}, status=400)
    process_image(file, service, 'product_jpg')  # Используется конфиг product_jpg для обработки
    service.save(update_fields=['image'])
    return JsonResponse({'success': True, 'url': service.image.url})

@login_required
@require_POST
def delete_service_image(request, business_slug, service_slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)
    service = get_object_or_404(Service, slug=service_slug, business=business)
    if service.image:
        service.image.delete(save=False)  # удаляем файл из хранилища
        service.image = None
        service.save(update_fields=['image'])
    return JsonResponse({'success': True})


@login_required
@require_POST
def upload_gallery_image(request, business_slug, model_type, model_slug):
    business = get_object_or_404(Business, slug=business_slug, owner=request.user)

    if model_type == "goods":
        model_class = Goods
        image_type_config = 'gallery'
    elif model_type == "service":
        model_class = Service
        image_type_config = 'gallery'
    else:
        return JsonResponse({'success': False, 'error': 'Invalid model type'}, status=400)

    obj = get_object_or_404(model_class, slug=model_slug, business=business)
    upload_file = request.FILES.get('image')

    if not upload_file:
        return JsonResponse({'success': False, 'error': 'No file provided'}, status=400)

    try:
        processed_path = process_image(upload_file, obj, image_type_config)

        if not processed_path:
            return JsonResponse({'success': False, 'error': 'Image processing failed, no file path returned'}, status=500)

        media = Media.objects.create(content_object=obj, order=obj.gallery.count())
        media.file.name = processed_path
        media.save(update_fields=['file'])

    except Exception as e:
        # Логируйте ошибку при необходимости
        # logger.error(f"Image upload processing error: {e}")
        return JsonResponse({'success': False, 'error': f'Image processing error: {str(e)}'}, status=500)

    return JsonResponse({'success': True, 'url': media.file.url, 'media_id': str(media.id)})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from apps.business.models import Media

@login_required
@require_POST
def delete_gallery_image(request, media_id):
    media = get_object_or_404(Media, id=media_id)

    try:
        if media.file and media.file.storage.exists(media.file.name):
            media.file.delete(save=False)
        media.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
