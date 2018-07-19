from django.contrib import admin
from django.urls import path, re_path
from django.http import HttpResponse, HttpResponseNotFound
from . import views

app_name ='board'
urlpatterns = [
	path('likesUpdate/', views.likesUpdate, name='likesUpdate'),
	path('addToCart/', views.add_to_cart_ajax, name='add_to_cart'),
	path('write/', views.user_write_board, name='user_write_board'),
	path('boardRemove/<author>/<board_pk>/', views.board_remove, name='board_remove'),
	path('boardEdit/<author>/<board_pk>/', views.board_edit, name='board_edit'),
	path('imageDelete/', views.image_delete, name='image_delete'),
	re_path(r'^(?P<pk>\d+)/$', views.view_board, name='view_board'),
	re_path(r'^(?P<pk>\d+)/(?P<comment_pk>\d+)/$', views.view_board, name='view_board_withcomment'),
	re_path(r'^(?P<pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/edit_ajax/$', views.comment_edit_ajax, name='comment_edit_ajax'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/delete_ajax/$', views.comment_delete_ajax, name='comment_delete_ajax')
	
]	
