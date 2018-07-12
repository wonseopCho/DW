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
from .models import Comment, Recommendation, Image
from DW import keys
import json, re

class ImageInlineAdmin(admin.TabularInline):
    model = Image

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()


class ImagesMultiuploadMixing(object):
    multiupload_maxfilesize = 6 * 2 ** 20 # 6 Mb
    def process_uploaded_file(self, uploaded, recommendation, request):
        if recommendation:
            image = recommendation.images.create(file=uploaded)
        else:
            image = Image.objects.create(file=uploaded, recommendation=None)
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

class ImageAdmin(ImagesMultiuploadMixing, MultiUploadAdmin):
    multiupload_form = True
    multiupload_list = True
    list_display = ['id', 'recommendation', 'recommendation_id', 'file', 'thumnails', 'author', 'created_at', 'updated_at']
    list_display_links = ['recommendation']

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()

class RecommendationAdmin(ImagesMultiuploadMixing, MultiUploadAdmin, SummernoteModelAdmin):
    formfield_overrides = {
    	models.TextField : {'widget': Textarea(attrs={'rows':1, 'cols':100})},
    }
    inlines = [ImageInlineAdmin,]
    multiupload_form = True
    multiupload_list = True
    search_fields = ['category__category','name']
    list_display = ['id', 'category', 'name', 'slug', 'likes_counts', 'author', 'created_at', 'updated_at']
    list_display_links = ['id', 'category', 'name']
    summernote_fields = ['about', 'information', 'contact']
    
    def delete_file(self, pk, request):
        '''
        Delete an image.
        '''
        obj = get_object_or_404(Image, pk=pk)
        return obj.delete()

    def likes_counts(self, recommendation):
        return '{}'.format(recommendation.likes.count())

    def save_model(self, request, obj, form, change):
        max_length = 50
        slug = slugify(strip_tags(obj.about), allow_unicode=True)
        slug = slug.replace('nbsp','-')
        if len(slug) <= max_length:
            obj.slug = slug
        trimmed_slug = slug[:max_length].rsplit('-', 1)[0]
        if len(trimmed_slug) <= max_length:
            obj.slug = trimmed_slug
        # First word is > max_length chars, so we have to break it
        obj.slug = slug[:max_length]+'...'

        if change :
            try :
                recommendation = Recommendation.objects.get(name=obj.name)
                img = Image.objects.filter(recommendation=recommendation).first()
                imgUrl = img.file.url
            except :
                imgUrl = ''
        else :
            imgUrl = ''
        if not obj.author:
            obj.author = request.user
        if obj.push_update:
            users = UserProfile.objects.all()
            for user in users:
                if user.subscription != None and user.subscription != "":                 
                    try:
                        webpush(
                            subscription_info=json.loads(user.subscription),
                            data="recommendation/"+str(obj.id)+"^"+obj.name+"^"+imgUrl,
                            vapid_private_key=keys.SERVICE_WORKER_PUSH_PRIVATE_KEY,
                            vapid_claims={"sub": "mailto:YourNameHere@example.org",}
                        )
                        print("push",obj.push_update, change)
                    except WebPushException as ex:
                        print("I'm sorry, Dave, but I can't do that: {}", repr(ex))
                        # Mozilla returns additional information in the body of the response.
                        if ex.response and ex.response.json():
                            extra = ex.response.json()
                            print("Remote service replied with a {}:{}, {}",
                                  extra.code,
                                  extra.errno,
                                  extra.message
                                  )
        obj.push_update = False
        obj.save()

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'recommendation','recommendation_id', 'parent', 'parent_author', 'group', 'seq_in_group', 'depth', 'author', 'message', 'created_at', 'updated_at']
    list_display_links = ['id', 'recommendation','recommendation_id', 'parent', 'parent_author', 'group', 'depth', 'author', 'message']

admin.site.register(Image, ImageAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Comment, CommentAdmin)