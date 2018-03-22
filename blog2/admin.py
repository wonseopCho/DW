from django.contrib import admin
from .models import Post, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ['id', 'title']

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
	list_display = ['id', 'post','post_id', 'author', 'message']

admin.site.register(Comment, CommentAdmin)