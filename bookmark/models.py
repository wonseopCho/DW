from django.db import models, connection

class Bookmark(models.Model):
	title = models.CharField(max_length=100, blank=True)
	url = models.URLField(unique=True)

	def __str__(self):
		return self.title

	"""docstring for Bookmark"models.Modelf
	title - models.CharField(max_mength-100, blank=True)
	url = models,URLField(unique=True)

	def __str__(self);
		return self.title:
		__init__(self, arg):
		super(Bookmark,models.Model._
		title - models.CharField(max_mength-100, blank=True)
		url = models,URLField(unique=True)

		def __str__(self);
			return self.title:
			_init__()
		self.arg = arg
	"""
