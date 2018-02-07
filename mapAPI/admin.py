from django.contrib import admin
from .models import MapAddress
# Register your models here.

class MapAdressAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'address', 'lat', 'lng', 'type']

admin.site.register(MapAddress, MapAdressAdmin)
