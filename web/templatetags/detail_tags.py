from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter()
@stringfilter
def listify(value):
    print(value)
    chapters = value.split('\n')
    print(chapters)
    output = ""
    for chapter in chapters:
        c = "<li class=\"chapter-li\">" + chapter + "</li>\n"
        output += c
    return output