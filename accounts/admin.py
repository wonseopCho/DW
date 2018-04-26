from django.contrib import admin
from .models import UserProfile, Friend

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['pk','id','user','firstname','lastname','article_cart_counts','gender', 'locale']

	def article_cart_counts(self, userProfile):
	        return '{}'.format(userProfile.article_cart.count())

admin.site.register(UserProfile,UserProfileAdmin)


class FriendAdmin(admin.ModelAdmin):
	list_display = ['id', 'current_user']

admin.site.register(Friend,FriendAdmin)
