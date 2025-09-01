
# ../apps/core/templatetags/fast_nav.py

from django import template
from django.urls import reverse

register = template.Library()

@register.inclusion_tag("core/includes/fast_scroll_nav.html", takes_context=True)
def render_fast_nav(context):
    """
    Формирует кнопки быстрого доступа:
    - авторизация пользователя
    - текущий путь
    Кнопки используют *.ico из /static/core/img/icons/
    """
    request = context["request"]
    user = request.user
    path = request.path

    buttons = {"left": None, "right": None}

    # Авторизованный пользователь
    if user.is_authenticated:
        if path.startswith(reverse("users:profile")):
            buttons["left"] = {"url": reverse("main:includes"), "icon": "home.png", "title": "Домой"}
            buttons["right"] = {"url": reverse("users:profile_edit"), "icon": "settings.png", "title": "Настройки"}
        elif path.startswith(reverse("core:favorites")):
            buttons["left"] = {"url": reverse("main:includes"), "icon": "home.png", "title": "Домой"}
            buttons["right"] = {"url": reverse("users:profile_edit"), "icon": "profile.png", "title": "Профиль"}
        else:
            buttons["left"] = {"url": reverse("core:favorites"), "icon": "favorites.png", "title": "Избранное"}
            buttons["right"] = {"url": reverse("users:profile_edit"), "icon": "profile.png", "title": "Профиль"}

    # Неавторизованный пользователь
    else:
        if path.startswith(reverse("users:login")):
            buttons["left"] = {"url": reverse("main:includes"), "icon": "home.png", "title": "Домой"}
            buttons["right"] = {"url": reverse("users:register"), "icon": "register.png", "title": "Регистрация"}
        else:
            buttons["left"] = {"url": reverse("main:includes"), "icon": "home.png", "title": "Домой"}
            buttons["right"] = {"url": reverse("users:login"), "icon": "login.png", "title": "Войти"}

    return {"left_btn": buttons["left"], "right_btn": buttons["right"]}

