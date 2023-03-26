from urllib.parse import urlencode

from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.staticfiles.storage import staticfiles_storage

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
    return staticfiles_storage.url('img/noposter.png')


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


@register.filter()
@stringfilter
def listify(value):
    value = value.replace("<", "").replace(">", "")
    chapters = value.split("\n")
    output = ""
    for chapter in chapters:
        if chapter and not chapter.isspace():
            classes = []
            if chapter.startswith("|"):
                classes.extend(["font-bold", "my-2", "text-lg", "underline"])
                chapter = f"{chapter.replace('|', '').title()} arc starts here"

            c = f'<p class="{" ".join(classes)}">{chapter.strip()}</p>\n'

            output += c
    return output.strip()
