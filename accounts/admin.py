from django.contrib import admin
from .models import UserProfile, Friend

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['pk','id','user', 'subscribe','article_cart_counts', 'recommand_cart_counts', 'board_cart_counts', 'qna_cart_counts', 'gender', 'locale']

	def subscribe(self, userProfile):
		print(userProfile.subscription)
		if userProfile.subscription != None and userProfile.subscription != "":
			return 'Yes'
		else:
			return 'No' 



	def article_cart_counts(self, userProfile):
	    return '{}'.format(userProfile.article_cart.count())

	def recommand_cart_counts(self, userProfile):
	    return '{}'.format(userProfile.recommendation_cart.count())

	def board_cart_counts(self, userProfile):
	    return '{}'.format(userProfile.board_cart.count())

	def qna_cart_counts(self, userProfile):
	    return '{}'.format(userProfile.board_cart.count())

admin.site.register(UserProfile,UserProfileAdmin)


class FriendAdmin(admin.ModelAdmin):
	list_display = ['id', 'current_user']

admin.site.register(Friend,FriendAdmin)
