from django import template

register = template.Library()

@register.filter
def to_lowercase(value, arg):
    return f'{arg}: {value.upper()}'