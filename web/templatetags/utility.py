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
    return str(value).capitalize()

@register.simple_tag
def active_tab(value, expected):
    active = str(value).split('/')
    if active[1] == expected:
        return "text-white px-3 py-2 rounded-md text-sm font-medium"
    return "text-gray-300 hover:text-white hover:text-white px-3 py-2 rounded-md text-sm font-medium"
