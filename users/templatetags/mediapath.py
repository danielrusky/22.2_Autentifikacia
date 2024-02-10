from django import template

from config.settings import MEDIA_URL

register = template.Library()


@register.simple_tag
def mediapath(val):
    if val:
        return f'/media/{val}'
    return '/media/no_photo.jpg'
