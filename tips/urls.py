from django.contrib import admin
from django.urls import path,re_path
from django.http import HttpResponse, HttpResponseNotFound
from . import views

app_name ='tips'
urlpatterns = [
	path('subway/', views.subway, name='subway'),
	path('listicle_admin/', views.listicle_admin, name='listicle_admin'),
	path('likesUpdate/', views.likesUpdate, name='likesUpdate'),
	path('articleText_call/', views.articleText_call, name='articleText_call'),
	path('addToCart/', views.add_to_cart_ajax, name='add_to_cart'),
	path('write/', views.user_write_tip, name='user_write_tip'),
	path('titleCheckAjax/', views.title_check_ajax, name='title_check_ajax'),
	path('titleCheckAjax/<article_pk>/', views.title_check_ajax, name='title_check_ajax'),
	path('articleRemove/<author>/<article_pk>/', views.article_remove, name='article_remove'),
	path('articleEdit/<author>/<article_pk>/', views.article_edit, name='article_edit'),
	path('imageDelete/', views.image_delete, name='image_delete'),
	re_path(r'^(?P<pk>\d+)/$', views.view_tips, name='view_tips'),
	re_path(r'^(?P<pk>\d+)/(?P<comment_pk>\d+)/$', views.view_tips, name='view_tips_withcomment'),
	re_path(r'^listicle/(?P<listicle_pk>\d+)/$', views.view_listicle, name='view_listicle'),
	re_path(r'^listicle/(?P<listicle_pk>\d+)/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', views.view_listicle, name='view_listicle_withcomment'),
	re_path(r'^(?P<pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/edit_ajax/$', views.comment_edit_ajax, name='comment_edit_ajax'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/delete_ajax/$', views.comment_delete_ajax, name='comment_delete_ajax'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]	
