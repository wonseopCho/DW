from django import template

register = template.Library()

@register.filter
def _replace(value):
	return value.replace("-"," ")

@register.filter
def replace_sq(value):
	return value.replace("\"","\'")

@register.filter
def get_fields(obj):
    return obj._meta.get_fields()
# ex> 
# {% for k in obj|get_fields %}
#     {{k}} <br>
# {% endfor %}