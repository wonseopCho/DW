from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse, HttpResponseNotFound
from . import views


app_name = "recommendation"
urlpatterns = [
	path('likesUpdate/', views.likesUpdate, name='likesUpdate'),
	path('addToCart/', views.add_to_cart_ajax, name='add_to_cart'),
	re_path(r'^(?P<pk>\d+)/$', views.view_recommendation, name='view_recommendation'),
	re_path(r'^(?P<pk>\d+)/(?P<comment_pk>\d+)/$', views.view_recommendation, name='view_tips_withcomment'),
	re_path(r'^(?P<pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/edit_ajax/$', views.comment_edit_ajax, name='comment_edit_ajax'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/delete_ajax/$', views.comment_delete_ajax, name='comment_delete_ajax')
]
