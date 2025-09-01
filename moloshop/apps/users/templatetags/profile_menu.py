
# apps/users/templatetags/profile_menu.py

from django import template
from apps.users.models.menu import ProfileMenuCategory


register = template.Library()

@register.inclusion_tag("users/components/user_menu.html", takes_context=True)
def render_user_menu(context):
    request = context['request']
    current_path = request.path
    all_items = ProfileMenuCategory.objects.all().prefetch_related('parent', 'children__children')
    menu_sections = [item for item in all_items if item.parent is None]

    def get_open_ids(path):
        for item in all_items:
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