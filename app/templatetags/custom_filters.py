from django import template
from django.utils.html import linebreaks

register = template.Library()

@register.filter
def custom_linebreaks(value):
    return linebreaks(value)