
# apps/users/templatetags/profile_menu.py

from django import template
from django.db.models import Q, Prefetch
from apps.users.models.menu import ProfileMenuCategory

register = template.Library()

@register.inclusion_tag("users/components/user_menu.html", takes_context=True)
def render_user_menu(context):
    request = context['request']
    current_path = request.path

    if request.user.is_authenticated:
        # Загружаем только корневые пункты меню, общие и персональные для пользователя
        menu_sections = ProfileMenuCategory.objects.filter(
            Q(user__isnull=True) | Q(user=request.user),
            parent=None
        ).order_by('order').prefetch_related(
            Prefetch('children', queryset=ProfileMenuCategory.objects.filter(
                Q(user__isnull=True) | Q(user=request.user)
            ).order_by('order'))
        )
    else:
        menu_sections = ProfileMenuCategory.objects.filter(
            user__isnull=True,
            parent=None
        ).order_by('order').prefetch_related('children')

    def get_open_ids(path):
        # Найти пункт меню по текущему пути и собрать список всех родителей для раскрытия
        for item in ProfileMenuCategory.objects.all():
            if item.get_absolute_url() == path:
                open_ids = []
                current = item.parent
                while current:
                    open_ids.append(current.id)
                    current = current.parent
                return open_ids
        return []

    open_ids = get_open_ids(current_path)

    return {
        'menu_sections': menu_sections,
        'request': request,
        'current_path': current_path,
        'open_ids': open_ids,
    }

