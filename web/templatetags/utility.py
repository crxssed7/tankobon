from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag
def urlparams(*_, **kwargs):
    safe_args = {k: v for k, v in kwargs.items() if v is not None}
    if safe_args:
        return f"?{urlencode(safe_args)}"
    return ""


@register.simple_tag
def capitalize(value):
    return str(value).title()


@register.simple_tag
def active_tab(value, expected):
    active = str(value).split("/")
    if active[1] == expected:
        return "text-white px-3 py-2 rounded-md text-sm font-medium"
    return "text-gray-300 hover:text-white hover:text-white px-3 py-2 rounded-md text-sm font-medium"


@register.simple_tag
def poster_url(record):
    if record.poster_file:
        return record.poster_file.url
    return ""


@register.simple_tag
def banner_url(record):
    if record.banner_file:
        return record.banner_file.url
    return ""


@register.simple_tag
def collected(volume, user):
    return volume.has_collected(user=user)


@register.simple_tag
def get_field_value(record, field):
    if hasattr(record, field):
        value = getattr(record, field)
        if value:
            return value
    return "Unknown"
