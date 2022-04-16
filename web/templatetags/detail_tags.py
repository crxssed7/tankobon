from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter()
@stringfilter
def listify(value):
    chapters = value.split('\n')
    output = ""
    for chapter in chapters:
        if not chapter.isspace():
            c = "<li class=\"chapter-li\">" + chapter + "</li>\n"
            output += c
    return output