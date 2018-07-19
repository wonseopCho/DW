from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.conf import settings
from multiupload.admin import MultiUploadAdmin
from django_summernote.admin import SummernoteModelAdmin
from pywebpush import webpush, WebPushException
from accounts.models import UserProfile
from django.contrib.auth.models import User
from .models import Board, Image, Comment
import json, re

class ImageInlineAdmin(admin.TabularInline):
    model = Image

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()

class ImagesMultiuploadMixing(object):
    multiupload_maxfilesize = 6 * 2 ** 20 # 6 Mb
    def process_uploaded_file(self, uploaded, article, request):
        if article:
            image = article.images.create(file=uploaded)
        else:
            image = Image.objects.create(file=uploaded, article=None)
        return {
            'url': image.file.url,
            'thumbnail_url': image.file.url,
            'id': image.id,
            'name': image.filename
        }

        def save_model(self, request, obj, form, change):
            if not obj.author:
                obj.author = request.user
            obj.save()

class BoardAdmin(ImagesMultiuploadMixing, MultiUploadAdmin, SummernoteModelAdmin):
    formfield_overrides = {
        models.TextField : {'widget': Textarea(attrs={'rows':1, 'cols':100})},
    }
    inlines = [ImageInlineAdmin,]
    multiupload_form = True
    multiupload_list = True
    search_fields = ['id', 'b_title']
    list_display = ['id', 'b_title', 'video', 'slug', 'rating', 'views', 'likes_counts', 'author', 'created_at', 'updated_at']
    list_display_links = ['id', 'b_title']
    summernote_fields = ['text']
    
    def delete_file(self, pk, request):
        '''
        Delete an image.
        '''
        obj = get_object_or_404(Image, pk=pk)
        return obj.delete()

    def likes_counts(self, article):
        return '{}'.format(article.likes.count())

    def save_model(self, request, obj, form, change):
        max_length = 48
        slug = slugify(strip_tags(obj.text), allow_unicode=True)
        slug = slug.replace('nbsp','-')
        if len(slug) <= max_length:
            obj.slug = slug
        trimmed_slug = slug[:max_length].rsplit('-', 1)[0]
        if len(trimmed_slug) <= max_length:
            obj.slug = trimmed_slug
        # First word is > max_length chars, so we have to break it
        obj.slug = slug[:max_length]+'...'
        
        if not obj.author:
            obj.author = request.user

        obj.save()

class ImageAdmin(ImagesMultiuploadMixing, MultiUploadAdmin):
    multiupload_form = True
    multiupload_list = True
    list_display = ['id', 'board', 'board_id', 'file', 'thumnails', 'author', 'created_at', 'updated_at']
    list_display_links = ['board']

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'board','board_id', 'parent', 'parent_author', 'group', 'seq_in_group', 'depth', 'author', 'message', 'created_at', 'updated_at']
    list_display_links = ['id', 'board','board_id', 'parent', 'parent_author', 'group', 'depth', 'author', 'message']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Image, ImageAdmin)