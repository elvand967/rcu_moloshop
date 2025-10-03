
# apps/users/context_processors.py

from django.db.models import Q, Prefetch
from apps.users.models.menu import ProfileMenuCategory

def user_menu(request):
    if request.user.is_authenticated:
        # Загружаем только корневые пункты меню (общие и персональные)
        global_roots = ProfileMenuCategory.objects.filter(user__isnull=True, parent=None).order_by('order')
        user_roots = ProfileMenuCategory.objects.filter(user=request.user, parent=None).order_by('order')

        roots = global_roots | user_roots

        # Предзагружаем потомков с соответствующей фильтрацией
        menu_sections = []
        for root in roots:
            if root.user is None:
                descendants = root.get_descendants(include_self=True).filter(user__isnull=True)
            else:
                descendants = root.get_descendants(include_self=True).filter(user=request.user)
            menu_sections.extend(descendants)
    else:
        menu_sections = ProfileMenuCategory.objects.filter(user__isnull=True).order_by('tree_id', 'lft')

    return {
        'menu_sections': menu_sections,
        'current_path': request.path,
        'open_ids': [],  # Здесь можно добавить логику запоминания раскрытых пунктов
    }




