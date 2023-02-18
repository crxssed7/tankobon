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
            classes = []
            if chapter.startswith("|"):
                classes.extend(["font-bold", "my-2", "text-lg", "underline"])
                chapter = f"{chapter.replace('|', '').title()} arc starts here"

            c = f'<p class="{" ".join(classes)}">{chapter.strip()}</p>\n'

            output += c
    return output.strip()
