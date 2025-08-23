# ../apps/core/utils/url_registry.py

from django.urls import get_resolver


def get_all_named_urls(app_names: list[str] | None = None) -> list[tuple[str, str]]:
    """
    Возвращает список (url_name, url_name) для использования в choices формы.
    Если указан список app_names, фильтрует только их.

    Пример использования:
    В ../apps/core/forms/footer_menu.py:
        self.fields['url'].choices = get_all_named_urls(app_names=['core', 'main'])
    """
    resolver = get_resolver()
    choices: list[tuple[str, str]] = []

    def walk_patterns(patterns, namespace: str | None = None):
        for p in patterns:
            # Вложенные include(...)
            if hasattr(p, 'url_patterns'):
                ns = f"{namespace}:{p.namespace}" if namespace and p.namespace else p.namespace or namespace
                walk_patterns(p.url_patterns, ns)
            else:
                # Только именованные маршруты
                if p.name:
                    full_name = f"{namespace}:{p.name}" if namespace else p.name
                    # Фильтруем по app_names (берём первый уровень namespace)
                    if not app_names or (namespace and namespace.split(":")[0] in app_names):
                        choices.append((full_name, full_name))

    walk_patterns(resolver.url_patterns)
    # Убираем дубликаты и сортируем
    return sorted(set(choices), key=lambda x: x[0])
