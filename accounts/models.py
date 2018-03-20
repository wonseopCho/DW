from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=100, default='')
	city = models.CharField(max_length=100, default='')
	phone = models.IntegerField(default=0)

def create_profile(sender, **kwargs):
	if kwargs['created'] == True : # True = when created , False = when updated
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

# def delete_profile(sender, **kwargs):
# 	user_profile = UserProfile.objects.filter(user=kwargs['instance']).delete()

post_save.connect(create_profile, sender=User)
# post_delete.connect(delete_profile, sender=User)


class Friend(models.Model):
	users = models.ManyToManyField(User)
	current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

	@classmethod
	def make_friend(cls, current_user, new_friend):
		friend, created = cls.objects.get_or_create(
			current_user = current_user
		)
		print('////////////////', friend, created)
		friend.users.add(new_friend)

	@classmethod
	def lose_friend(cls, current_user, new_friend):
		friend, created = cls.objects.get_or_create(
			current_user = current_user
		)
		friend.users.remove(new_friend)