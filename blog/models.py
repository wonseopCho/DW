from django.db import models
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(unique=True, allow_unicode=True)
	description = models.CharField(max_length=100, blank=True)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, db_index=True)

	class Meta:
		ordering = ['-updated_at']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:postDV', args=[self.slug])
		#return '/blog/post/%s' % self.slug

# Create your models here.
