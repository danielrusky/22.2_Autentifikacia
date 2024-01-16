from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def mediapath(val):
    if val:
        return f'/media/{val}'
    return '/media/no_photo.jpg'
