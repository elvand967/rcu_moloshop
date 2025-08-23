# ../apps/core/templatetags/footer_menu.py

from django import template
from apps.core.models.footer_menu import FooterMenuCategory

register = template.Library()


@register.inclusion_tag("core/includes/footer_menu.html", takes_context=True)
def render_footer_menu(context):
    """
    Рендерит меню подвала: только активные родительские и дочерние элементы.
    """
    request = context["request"]
    parents = FooterMenuCategory.objects.filter(parent__isnull=True, is_active_link=True).order_by("order")

    return {
        "parents": parents,
        "request": request,
    }
