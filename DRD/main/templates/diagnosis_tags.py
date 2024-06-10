from django import template

register = template.Library()

@register.simple_tag
def compare_values(val1, val2):
    return val1 == val2
