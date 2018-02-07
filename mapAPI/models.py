from django.db import models
from django.urls import reverse

# Create your models here.

class MapAddress(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=60)
	address = models.CharField(max_length=80)
	lat = models.FloatField(null=True, blank=True)
	lng = models.FloatField(null=True, blank=True)
	type = models.CharField(max_length=30)

	def __str__(self):
		return self.name
