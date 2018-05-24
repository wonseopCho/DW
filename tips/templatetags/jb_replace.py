from django import template

register = template.Library()

@register.filter
def _replace(value):
	return value.replace("-"," ")

@register.filter
def replace_sq(value):
	return value.replace("\"","\'")