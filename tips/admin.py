from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import Category, Image
from multiupload.admin import MultiUploadAdmin

class ImageInlineAdmin(admin.TabularInline):
    model = Image

class ImagesMultiuploadMixing(object):
    multiupload_maxfilesize = 6 * 2 ** 20 # 6 Mb
    def process_uploaded_file(self, uploaded, category, request):
        if category:
            image = category.images.create(file=uploaded)
        else:
            image = Image.objects.create(file=uploaded, category=None)
        return {
            'url': image.file.url,
            'thumbnail_url': image.file.url,
            'id': image.id,
            'name': image.filename
        }

class CategoryAdmin(ImagesMultiuploadMixing, MultiUploadAdmin):
    inlines = [ImageInlineAdmin,]
    multiupload_form = True
    multiupload_list = True
    list_display = ['id', 'category', 'title', 'created_at', 'updated_at']

    def delete_file(self, pk, request):
        '''
        Delete an image.
        '''
        obj = get_object_or_404(Image, pk=pk)
        return obj.delete()


class ImageAdmin(ImagesMultiuploadMixing, MultiUploadAdmin):
    multiupload_form = False
    multiupload_list = True
    list_display = ['id', 'category', 'category_id', 'file', 'created_at', 'updated_at']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)