# moloshop/apps/core/templatetags/string_filters.py
from django import template

register = template.Library()


@register.filter
def startswith(value, prefix: str) -> bool:
    """
    Проверяет, начинается ли строка на prefix.
    Пример: {{ "https://ya.ru"|startswith:"http" }} -> True
    """
    if not isinstance(value, str):
        return False
    return value.startswith(prefix)


@register.filter
def endswith(value, suffix: str) -> bool:
    """
    Проверяет, оканчивается ли строка на suffix.
    Пример: {{ "file.txt"|endswith:".txt" }} -> True
    """
    if not isinstance(value, str):
        return False
    return value.endswith(suffix)
