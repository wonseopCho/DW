from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from tips.models import Category

class Recommendation(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, blank=False, null=False, on_delete=models.CASCADE)
    name = models.TextField(blank=False, null=False, max_length=100)
    video = models.FileField(blank=True, upload_to='recommendation/video/%Y/%m/%d')
    slug = models.SlugField(max_length=100, unique=False, editable=False, allow_unicode=True)
    about = models.TextField(blank=False, null=False)
    information = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)
    phone_num = models.TextField(blank=True, max_length=100)
    address = models.TextField(blank=True, null=True, max_length=300)
    author = models.ForeignKey(User, blank=True, null=True, editable=False, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL ,blank=True, editable=False, related_name='recommendation_likes')
    push_update = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
	    return self.name

    def get_absolute_url(self):
	    return reverse('recommendation:view_recommendation', args=[self.pk])

class Comment(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    parent = models.PositiveIntegerField(blank=False, null=True, default=None)
    parent_author = models.CharField(blank=False, null=True, default=None, max_length=100)
    group = models.PositiveIntegerField(blank=False, default=None)
    seq_in_group = models.PositiveIntegerField(blank=False, default=0)
    depth = models.PositiveIntegerField(default=1)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='recom_comment_author', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [ 'group', 'seq_in_group' ]

    def get_absolute_url(self):
        return reverse('recommendation:view_recommendation', args=[self.recommendation.pk])

    def get_edit_url(self):
        return reverse('recommendation:comment_edit', args=[self.recommendation.pk, self.pk])

    def get_delete_url(self):
        return reverse('recommendation:comment_delete', args=[self.recommendation.pk, self.pk])

class Image(models.Model):
    file = models.FileField(upload_to='recommendation/images/%Y/%m/%d')
    thumnails = ImageSpecField(source='file', 
							   processors=[ResizeToFill(200,112)],
							   options={'quality': 100})
    recommendation = models.ForeignKey(Recommendation, blank=True, null=True, related_name="images", on_delete=models.CASCADE)
    # !!!VIP!!! as we are going to use multiupload package for django, in order to call images in template page just simply call images.all not like image_set which is typcal way!!!! 
    author = models.ForeignKey(User, blank=True, null=True, editable=False, related_name='recom_image_author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

    @property
    def filename(self):
        return self.file.name.rsplit('/', 1)[-1]