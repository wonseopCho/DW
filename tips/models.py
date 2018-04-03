from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, unique=True, blank=False)
    author = models.ForeignKey(User, blank=True, null=True, editable=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField('Title', unique=True, max_length=100)
    video = models.FileField(blank=True, upload_to='tips/video/%Y/%m/%d')
    slug = models.SlugField(max_length=41, unique=False, allow_unicode=True)
    text = models.TextField()
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL ,blank=True, related_name='category_likes')
    author = models.ForeignKey(User, blank=True, null=True, editable=False,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
    	ordering = ['-id']

    def __str__(self):
        return self.title


class Image(models.Model):
    file = models.FileField(upload_to='tips/images/%Y/%m/%d')
    thumnails = ImageSpecField(source='file', 
							   processors=[ResizeToFill(100,100)],
							   format='JPEG',
							   options={'quality': 60})
    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, blank=True, null=True, editable=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

    @property
    def filename(self):
        return self.file.name.rsplit('/', 1)[-1]

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author