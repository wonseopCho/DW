from django.contrib.auth.views import(
	login,
	password_reset,
	password_reset_done,
	password_reset_confirm,
	password_reset_complete,
	)
from django.contrib import admin
from django.urls import path, re_path
from tips.models import Article, Category
from . import views

app_name = 'accounts'
args = {'categories' : Category.objects.all()}
urlpatterns = [
	re_path(r'^\w*$', views.login_redirect, name='login_redirect'),
	path('connect/<operation>/<pk>', views.change_friends, name='change_friends'),
	path('login/', login, {'template_name':'login.html','extra_context': args}, name='account_login'),
	path('register/', views.register, name='register'),
	path('register/done', views.UserCreateDoneTemplate.as_view(), name='register_done'),
	path('register/usernameCheckAjax', views.usernameCheckAjax, name='usernameCheckAjax'),
	path('register/emailCheckAjax', views.emailCheckAjax, name='emailCheckAjax'),
	# path('register/activate/<uidb64>/<token>/', views.UserActivate, name='register_activate'),
	re_path(r'^register/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.UserActivate, name='register_activate'),
	path('register/activate/complete/', views.register_complete, name='register_complete'),
	path('profile/', views.view_profile, name='view_profile'),
	path('profile/<pk>/', views.view_profile, name='view_profile_with_pk'),
	path('profile/edit/<pk>/', views.edit_profile, name='edit_profile'),
	path('profile/password/', views.change_password),
	path('profile/articleRemove', views.articleRemove, name="articleRemove"),
	path('change-password/', views.change_password, name='change_password'),
	path('reset-password/', password_reset, {
		'template_name': 'manual_registration/password_reset_form.html',
		'email_template_name': 'manual_registration/password_reset_email.html',
     	'subject_template_name': 'manual_registration/password_reset_subject.txt',
		'post_reset_redirect': 'accounts:password_reset_done','extra_context': args
		}, 
		name='reset_password'),
	path('reset-password/done/', password_reset_done, { 
		'template_name': 'manual_registration/password_reset_done.html','extra_context': args
		}, 
		name='password_reset_done'),
	path('reset-password/confirm/<uidb64>/<token>/', password_reset_confirm, {
		'template_name': 'manual_registration/password_reset_form.html',
		'post_reset_redirect': 'accounts:password_reset_complete','extra_context': args
		}, 
		name='password_reset_confirm'),
	# re_path(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {
	# 	'template_name': 'manual_registration/password_reset_form.html',
	# 	'post_reset_redirect': 'accounts:password_reset_complete',
	# 	}, 
	# 	name='password_reset_confirm'),
	path('reset-password/complete/', password_reset_complete, {
		'template_name': 'manual_registration/password_reset_complete.html','extra_context': args
		}, 
		name='password_reset_complete'),
	path('subscribe/', views.subscribe, name='subscribe')

]