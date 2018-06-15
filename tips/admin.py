from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.conf import settings
from multiupload.admin import MultiUploadAdmin
from django_summernote.admin import SummernoteModelAdmin
from pywebpush import webpush, WebPushException
from accounts.models import UserProfile
from django.contrib.auth.models import User
from .models import Listicle, Category, Article, Image, Comment
from .forms import ListicleForm, ArticleForm
from DW import keys
import json, re

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'image', 'color', 'author', 'created_at', 'updated_at']
    list_display_links = ['id', 'category']

    def save_model(self, request, obj, form, change):
        first = obj.category[0].upper()
        rest = obj.category[1:].lower()
        obj.category = first+rest
        if not obj.author:
            obj.author = request.user
        obj.save()

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

class ArticleAdmin(ImagesMultiuploadMixing, MultiUploadAdmin, SummernoteModelAdmin):
    form = ArticleForm
    inlines = [ImageInlineAdmin,]
    multiupload_form = True
    multiupload_list = True
    search_fields = ['id','title']
    list_display = ['id', 'category', 'title', 'video', 'slug', 'rating', 'views', 'likes_counts', 'author', 'created_at', 'updated_at']
    list_display_links = ['id', 'category', 'title']
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
        reg = re.compile('(?<=<img src=")(/\w*/\w*-*\w*/\d{4}-\d{2}-\d{2}/\w*-\w*-\w*-\w*-\w*.\w+)(?=")')
        img = reg.search(obj.text)
        if img != None:
            imgUrl = img.group()
        else:
            imgUrl = ''
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

        if obj.push_update:
            users = UserProfile.objects.all()
            for user in users:
                if user.subscription != None and user.subscription != "":                 
                    try:
                        webpush(
                            subscription_info=json.loads(user.subscription),
                            data="tips/"+str(obj.id)+"^"+obj.title+"^"+imgUrl,
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

class ImageAdmin(ImagesMultiuploadMixing, MultiUploadAdmin):
    multiupload_form = False
    multiupload_list = True
    list_display = ['id', 'article', 'article_id', 'file', 'thumnails', 'author', 'created_at', 'updated_at']
    list_display_links = ['article']

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'article','article_id', 'parent', 'parent_author', 'group', 'seq_in_group', 'depth', 'author', 'message', 'created_at', 'updated_at']
    list_display_links = ['id', 'article','article_id', 'parent', 'parent_author', 'group', 'depth', 'author', 'message']

class ListicleAdmin(admin.ModelAdmin):
    form = ListicleForm
    list_display = ['id', 'title', 'category', '_articles', 'author', 'image', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']

    def _articles(self, listicle):
        return 'Total#: {}'.format(listicle.articles.count())

    def save_model(self, request, obj, form, change):
        imgUrl = obj.image.url
        if not obj.author:
            obj.author = request.user
        if obj.push_update:
            users = UserProfile.objects.all()
            for user in users:
                if user.subscription != None and user.subscription != "":                 
                    try:
                        webpush(
                            subscription_info=json.loads(user.subscription),
                            data="tips/listicle/"+str(obj.id)+"^"+obj.title+"^"+imgUrl,
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

admin.site.register(Listicle, ListicleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)