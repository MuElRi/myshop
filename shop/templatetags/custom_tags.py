from django import template

register = template.Library()

# Тег для получения значения по ключу из словаря
@register.filter
def key(dictionary, key_name):
    """Возвращает значение из словаря по ключу"""
    try:
        return dictionary[key_name]
    except (TypeError, KeyError):
        return None