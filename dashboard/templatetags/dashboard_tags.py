from django import template

register = template.Library()


@register.simple_tag
def dashboard_active_tab(value, expected):
    if value == expected:
        return "bg-hint text-blay font-bold"
    return "hover:bg-hint hover:text-blay hover:border-hint focus:bg-hint focus:blay focus:text-blay transition duration-300 ease-in-out"
