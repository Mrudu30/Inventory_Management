from django import template

register = template.Library()

@register.filter
def my_range(value):
    return range(value)
