from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from colorful.fields import RGBColorField

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, unique=True, blank=False)
    image = models.FileField(upload_to='tips/category/images/')
    color = RGBColorField()
    author = models.ForeignKey(User, blank=True, null=True, editable=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(unique=True, max_length=100)
    video = models.FileField(blank=True, upload_to='tips/video/%Y/%m/%d')
    slug = models.SlugField(max_length=100, unique=False, editable=False, allow_unicode=True)
    text = models.TextField(blank=False, null=False)
    rating = models.PositiveSmallIntegerField(blank=True, default=0, choices=[(i, i) for i in range(0, 6)], validators=[MaxValueValidator(5), MinValueValidator(0)])
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL ,blank=True, editable=False, related_name='category_likes')
    author = models.ForeignKey(User, blank=True, null=True, editable=False, on_delete=models.CASCADE)
    push_update = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
    	ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tips:view_tips', args=[self.pk])


class Image(models.Model):
    file = models.FileField(upload_to='tips/images/%Y/%m/%d')
    thumnails = ImageSpecField(source='file', 
							   processors=[ResizeToFill(200,112)],
							   format='JPEG',
							   options={'quality': 100})
    article = models.ForeignKey(Article, blank=True, null=True, related_name="images", on_delete=models.CASCADE)
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
    parent = models.PositiveIntegerField(blank=False, null=True, default=None)
    parent_author = models.CharField(blank=False, null=True, default=None, max_length=100)
    group = models.PositiveIntegerField(blank=False, default=None)
    seq_in_group = models.PositiveIntegerField(blank=False, default=0)
    depth = models.PositiveIntegerField(default=1)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [ 'group', 'seq_in_group' ]

    def get_absolute_url(self):
        return reverse('tips:view_tips', args=[self.article.pk])

    def get_edit_url(self):
        return reverse('tips:comment_edit', args=[self.article.pk, self.pk])

    def get_delete_url(self):
        return reverse('tips:comment_delete', args=[self.article.pk, self.pk])

class Listicle(models.Model):
    title = models.CharField('Title', blank=False, unique=True, max_length=100)
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.CASCADE)
    image = models.FileField(blank=False, null=False, upload_to='tips/listicle/images/%Y/%m/%d')
    thumnails = ImageSpecField(source='image', 
                               # processors=[ResizeToFill(200,100)],
                               format='JPEG',
                               options={'quality': 30})
    articles = models.ManyToManyField(Article, blank=False, related_name='listicle_articles')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=True, editable=False, on_delete=models.CASCADE)
    push_update = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return reverse('tips:view_listicle', args=[self.pk])

    def __str__(self):
        return self.title

