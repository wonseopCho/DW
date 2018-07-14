from django import forms
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from .models import UserProfile

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	terms = forms.BooleanField(
		label= 'Terms of sevice',
		widget=forms.CheckboxInput(
			attrs={
			'required':'True',
			}
		),
		# error_messages={
		# 	'required':'You must agree to the Terms of service to sign up',
		# }
	)
	privacy = forms.BooleanField(
		label='Privacy policy',
		widget=forms.CheckboxInput(
			attrs={
			'required': 'True',
			}
		),
		# error_messages={
		# 	'required':'You must agree to the Privacy policy to sign up',
		# }
	)

	# def __init__(self, *args, **kwargs):
	# 	# self.request = kwargs.pop('request', None)
	# 	super(UserCreationForm, self).__init__(*args, **kwargs)

	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
			]

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		
	# 	if commit:
	# 		user.active = False
	# 		user.save()
	# 		current_site = get_current_site(request)
	# 		subject = 'welcome to %s! Confirm your Email' % current_site
	# 		message = render_to_string('manual_registration/user_activate_email.html', {
	# 			'user': user,
	# 			'domain': current_site.domain,
	# 			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
	# 			'token': account_activation_token.make_token(user),
	# 			})
	# 		email = EmailMessage(subject, message, to=[user.email])
	# 		email.send()

		return user
class ExtraUserForm(forms.ModelForm):
	model = UserProfile
	exclude = ['user']

class EditProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = [
			'firstname',
			'lastname',
			'gender',
			'city',
			'locale',
			'phone',
			'picture',
			]
	#	exclud = []