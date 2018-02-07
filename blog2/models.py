from django.db import models

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	photo = models.ImageField(blank=True, null=True, upload_to="test/%Y/%m/%d")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.CharField(max_length=100)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

