from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from allauth.socialaccount.models import SocialAccount
from tips.models import Article
from recommendation.models import Recommendation

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=100, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	firstname = models.CharField(max_length=50, blank=True, null=True)
	lastname = models.CharField(max_length=50, blank=True, null=True)
	phone = models.IntegerField(default=0)
	picture = models.ImageField(blank=True, null=True, upload_to="accounts/user_profile/%Y/%m/%d")
	photo_url = models.CharField(max_length=200, blank=True, null=True)
	gender = models.CharField(max_length=10, blank=True, null=True)
	locale = models.CharField(max_length=50, blank=True, null=True)
	article_cart = models.ManyToManyField(Article, blank=True, related_name='user_articles')
	recommendation_cart = models.ManyToManyField(Recommendation, blank=True, related_name='user_recommendation')
	subscription = models.CharField(max_length=500, blank=True, null=True)

def create_profile(sender, **kwargs):
	if kwargs['created'] == True : # True = when created , False = when updated
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

# def delete_profile(sender, **kwargs):
# 	user_profile = UserProfile.objects.filter(user=kwargs['instance']).delete()

def save_profile(sender, instance, **kwargs):
	username = User.objects.get(username=instance)
	user_profile = UserProfile.objects.get(user=username)
	user_profile.photo_url = instance.get_avatar_url()
	try :
		user_profile.gender = instance.extra_data['gender']
		user_profile.locale = instance.extra_data['locale']
	except :
		user_profile.gender = ''
		user_profile.locale = ''

	user_profile.save()

post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=SocialAccount)
# post_delete.connect(delete_profile, sender=User)

class Friend(models.Model):
	users = models.ManyToManyField(User)
	current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

	@classmethod
	def make_friend(cls, current_user, new_friend):
		friend, created = cls.objects.get_or_create(
			current_user = current_user
		)
		friend.users.add(new_friend)

	@classmethod
	def lose_friend(cls, current_user, new_friend):
		friend, created = cls.objects.get_or_create(
			current_user = current_user
		)
		friend.users.remove(new_friend)