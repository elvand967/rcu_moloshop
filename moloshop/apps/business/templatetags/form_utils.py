
# apps/business/templatetags/form_utils.py

'''
Кастомный фильтр has_attr для безопасной проверки
'''

from django import template

register = template.Library()

@register.filter
def has_attr(obj, attr_name):
    """Проверяет, есть ли у объекта атрибут attr_name"""
    return hasattr(obj, attr_name)
