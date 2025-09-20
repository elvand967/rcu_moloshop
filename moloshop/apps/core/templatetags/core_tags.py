
# ../apps/core/templatetags/core_tags.py

from django import template
from django.templatetags.static import static
from django.urls import reverse
from apps.users.models.profile import UserProfile

register = template.Library()

@register.inclusion_tag('core/includes/main_menu.html', takes_context=True)
def core_tags_main_menu(context):
    user = context['request'].user
    menu_items = [
        {'title': "Главная", 'url_name': 'main:includes', 'children': []},
        {'title': "Сервисы", 'url_name': 'core:about', 'children': [
            {'title': "Портфолио", 'url_name': 'core:portfolio'},
            {'title': "Витрина", 'url_name': 'core:showcase', 'children': []},
            {'title': "Доска объявлений", 'url_name': 'core:board'},
        ]},
        {'title': "Блог", 'url_name': 'core:showcase', 'children': []},
        {'title': "FAG", 'url_name': 'core:fag', 'children': []},
    ]
    if user.is_authenticated:
        profile = getattr(user, 'profile', None)
        personal_menu = [
            {'title': "Профиль", 'url_name': 'users:profile_edit'},
            {'title': "Выйти", 'url_name': 'users:logout'},
            {'title': "Сменить пароль", 'url_name': 'users:password_change'},  # добавлена ссылка смены пароля
        ]
        if profile and profile.user_status == UserProfile.UserStatus.GUEST:
            personal_menu.insert(0, {'title': "Подтвердить email", 'url_name': 'users:verify_email'})
        menu_items.append({'title': "Личный кабинет", 'url_name': 'users:profile_edit', 'children': personal_menu})
    else:
        menu_items.append({'title': "Войти", 'url_name': 'users:login', 'children': [
            {'title': "Войти", 'url_name': 'users:login'},
            {'title': "Регистрация", 'url_name': 'users:register'},
        ]})
    return {'menu_items': menu_items}

