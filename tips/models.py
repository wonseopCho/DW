from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    
    id = models.AutoField(primary_key=True)
    category = models.CharField('Category', max_length=20)
    title = models.CharField('Title', unique=True, max_length=100)
    video = models.CharField(max_length=200)
    text = models.TextField()
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
    	ordering = ['-id']

    def __str__(self):
        return self.category


class Image(models.Model):
    file = models.FileField(upload_to='tips/images/')
    thumnails = ImageSpecField(source='file', 
							   processors=[ResizeToFill(100,100)],
							   format='JPEG',
							   options={'quality': 60})
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

    @property
    def filename(self):
        return self.file.name.rsplit('/', 1)[-1]
