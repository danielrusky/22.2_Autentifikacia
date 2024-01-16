from django import template
from django.utils.safestring import mark_safe
from config.settings import MEDIA_URL

register = template.Library()


@register.simple_tag
def media_tag(product):
    return MEDIA_URL + str(product)


@register.filter
def split(text):
    """Обрезает переданный текст до 100 символов"""
    result = text[0:100]
    return mark_safe(result)