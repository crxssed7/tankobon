from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def listify(value):
    value = value.replace("<", "").replace(">", "")
    chapters = value.split("\n")
    output = ""
    for chapter in chapters:
        if not chapter.isspace():
            if chapter.startswith("|"):
                c = (
                    "<br /><p><b>"
                    + chapter.replace("|", "")
                    + " arc starts here.</b></p>"
                )
            else:
                c = '<li class="chapter-li">' + chapter + "</li>\n"
            output += c
    return output
