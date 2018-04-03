from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import Category, Article, Image, Comment
from multiupload.admin import MultiUploadAdmin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'author', 'created_at', 'updated_at']
    list_display_links = ['id', 'category']

    def save_model(self, request, obj, form, change):
        obj.category = obj.category.lower()
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

class ArticleAdmin(ImagesMultiuploadMixing, MultiUploadAdmin):
    inlines = [ImageInlineAdmin,]
    multiupload_form = True
    multiupload_list = True
    search_fields = ['article','title']
    list_display = ['id', 'category', 'title', 'video', 'slug', 'views', 'likes_counts', 'author', 'created_at', 'updated_at']
    list_display_links = ['id', 'category', 'title']
    prepopulated_fields = {
        'slug' : ['text']
    }

    def delete_file(self, pk, request):
        '''
        Delete an image.
        '''
        obj = get_object_or_404(Image, pk=pk)
        return obj.delete()

    def likes_counts(self, article):
        return '{}'.format(article.likes.count())


    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
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
    list_display = ['id', 'article','article_id', 'author', 'message']

admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)