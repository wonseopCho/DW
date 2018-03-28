import logging
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth.forms import (
										PasswordChangeForm,
										UserChangeForm, 
										UserCreationForm,
										)
from .models import Friend, UserProfile
from .forms import (
					EditProfileForm, 
					RegistrationForm,
					)
from .tokens import account_activation_token

def UserActivate(request, uidb64, token):
    try:
   	    uid = urlsafe_base64_decode(uidb64).decode()
   	    user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return redirect('accounts:register_complete')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

class UserCreateDoneTemplate(TemplateView):
    template_name = 'manual_registration/register_done.html'

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.active = False
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your account'
			message = render_to_string('manual_registration/user_activate_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
				})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
            	mail_subject, message, to=[to_email])
			email.send()
			return HttpResponse('please confirm your email. address to complete the registration')
		else:
			return HttpResponse('username exists')
	else:
		form = RegistrationForm()
		return render(request, 'accounts/reg_form.html', {
			'form': form
			})

def register_complete(request):
	return render(request, 'manual_registration/user_activate_complete.html' )

def login_redirect(request):
	return redirect('home')

@login_required
def view_profile(request, pk=None):
	if pk:
		user = User.objects.get(pk=pk)
	else :
		user = request.user
	others = User.objects.exclude(id = request.user.id)
	if Friend.objects.filter(current_user=request.user).count() != 1:
		Friend.make_friend(current_user=request.user, new_friend=request.user)
		Friend.lose_friend(current_user=request.user, new_friend=request.user)
	friend = Friend.objects.get(current_user=request.user)
	friends_list = friend.users.all()
	args = {
			'user': user, 
			'others':others, 
			'friends_list':friends_list
			}
	return render(request, 'accounts/view_profile.html', args)

@login_required
def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('accounts:edit_profile')
	else:
		form = EditProfileForm(instance=request.user)
		args = {'form': form}
		return render(request, 'accounts/edit_profile.html', args)

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data = request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('accounts:edit_profile')
		else:
			return redirect('accounts:change_password')
	else:
		form = PasswordChangeForm(user=request.user)
		args = {'form': form }
		return render(request, 'accounts/change_password.html', args)

def change_friends(request, operation, pk):
	friend = User.objects.get(pk=pk)
	if operation == 'add':
		Friend.make_friend(request.user, friend)
	elif operation == 'remove':
		Friend.lose_friend(request.user, friend)
	return redirect('accounts:view_profile')