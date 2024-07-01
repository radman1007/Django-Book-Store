from django import template

register = template.Library()

@register.filter(name='get_up')
def to_uppercase(value, arg):
    return f'{arg}: {value.upper()}'