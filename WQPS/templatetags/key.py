from django import template
register = template.Library()
@register.filter
def key(d, key_name):
    return d[key_name]