import logging
from django.http import HttpResponse
from django.conf import settings
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
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.forms import (
										PasswordChangeForm,
										UserChangeForm, 
										UserCreationForm,
										)
from allauth.socialaccount.models import SocialAccount
from tips.models import Article, Category
from .models import Friend, UserProfile
from .forms import (
					EditProfileForm, 
					RegistrationForm,
					ExtraUserForm,
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
			user.is_active = False
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
			if settings.DEBUG:
				email = EmailMessage(
					mail_subject, message, to=[to_email])
				email.send()
			else :
				send_mail(
					mail_subject,
					message,
					settings.DEFAULT_FROM_EMAIL,
					[to_email],
					fail_silently=False,
					)
			return HttpResponse('please confirm your email. address to complete the registration')
		else:
			return HttpResponse('username exists')
	else:
		form = RegistrationForm()
		return render(request, 'accounts/reg_form.html', {
			'form': form,
			'categories' : Category.objects.all(),
			})

def usernameCheckAjax(request):
	if request.method == 'POST':
		username = request.POST['username']
		try :
			User.objects.get(username=username)
			res = 'exist'
		except :
			res = 'good'
		return HttpResponse(res)
	else:
		return HttpResponse('post_error')

def emailCheckAjax(request):
	if request.method == 'POST':
		email = request.POST['email']
		try :
			User.objects.get(email=email)
			print(User.objects.get(email=email))
			res = 'exist'
		except :
			res = 'good'
		return HttpResponse(res)
	else:
		return HttpResponse('post_error')

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
	try :
		socialaccount = SocialAccount.objects.get(user=request.user)
	except :
		socialaccount = None
	authenticated_user = UserProfile.objects.get(user=request.user)
	userarticle = Article.objects.filter(author=request.user).order_by('category')	
	others = User.objects.exclude(id = request.user.id)
	if Friend.objects.filter(current_user=request.user).count() != 1:
		Friend.make_friend(current_user=request.user, new_friend=request.user)
		Friend.lose_friend(current_user=request.user, new_friend=request.user)
	friend = Friend.objects.get(current_user=request.user)
	friends_list = friend.users.all()
	args = {
			'user': user, 
			'others':others, 
			'friends_list':friends_list,
			'authenticated_user':authenticated_user,
			'socialaccount': socialaccount,
			'userarticle' : userarticle,
			'categories' : Category.objects.all(),
			}
	return render(request, 'accounts/view_profile.html', args)

@login_required
def edit_profile(request, pk):
	authenticated_user = UserProfile.objects.get(user=request.user)
	try :
		socialaccount = SocialAccount.objects.get(user=request.user)
	except :
		socialaccount = None
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('accounts:view_profile')
	else:
		form = EditProfileForm(instance=request.user)
		args = {
				'form': form,
				'authenticated_user':authenticated_user,
				'socialaccount': socialaccount,
				'categories' : Category.objects.all(),
				}
		return render(request, 'accounts/edit_profile.html', args)

@login_required
def change_password(request):
	authenticated_user = UserProfile.objects.get(user=request.user)
	try :
		socialaccount = SocialAccount.objects.get(user=request.user)
	except :
		socialaccount = None
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('accounts:view_profile')
		else:
			return redirect('accounts:change_password')
	else:
		form = PasswordChangeForm(user=request.user)
		args = {
				'form': form,
				'authenticated_user':authenticated_user,
				'socialaccount': socialaccount,
				'categories' : Category.objects.all(),
				}
		return render(request, 'accounts/change_password.html', args)

@login_required
def articleRemove(request):
	if request.method == 'POST':
		user_pk = request.POST['user']
		article_pk = request.POST['pk']
		user = UserProfile.objects.get(pk=user_pk)
		article = Article.objects.get(id=article_pk)
		user.article_cart.remove(article)
		return HttpResponse(article.id)
	else:
		return HttpResponse('post_error')

def change_friends(request, operation, pk):
	friend = User.objects.get(pk=pk)
	if operation == 'add':
		Friend.make_friend(request.user, friend)
	elif operation == 'remove':
		Friend.lose_friend(request.user, friend)
	return redirect('accounts:view_profile')

@login_required
def subscribe(request):
	if request.method == 'POST':
		user = UserProfile.objects.get(user=request.user)
		user.subscription = request.POST['subscription'].replace('null', '"null"')
		user.save()
		return HttpResponse(1) #sucess
	else:
		return HttpResponse(0) #failed