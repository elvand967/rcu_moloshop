# apps/business/views/ajax_upload.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from apps.business.models import Business
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
