from django import template

register = template.Library()

@register.filter
def _replace(value):
	return value.replace("-"," ")