from django.contrib import admin
from .models import UserProfile, Friend

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['pk', 'id', 'user']

admin.site.register(UserProfile,UserProfileAdmin)


class FriendAdmin(admin.ModelAdmin):
	list_display = ['id', 'current_user']

admin.site.register(Friend,FriendAdmin)
