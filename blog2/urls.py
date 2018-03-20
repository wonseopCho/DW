from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'blog2'
urlpatterns = [
	path('', views.index, name='index'),
	re_path(r'^(?P<pk>\d+)/$', views.post_detail, name='detail'),
	re_path(r'^(?P<pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
	path('new/', views.post_new, name='post_new')
]