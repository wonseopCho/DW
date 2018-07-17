from django.contrib import admin
from django.urls import path, re_path
from django.http import HttpResponse, HttpResponseNotFound
from . import views

app_name ='qna'
urlpatterns = [
	path('likesUpdate/', views.likesUpdate, name='likesUpdate'),
	path('addToCart/', views.add_to_cart_ajax, name='add_to_cart'),
	path('qnaRemove/<author>/<qna_pk>/', views.qna_remove, name='qna_remove'),
	path('qnaEdit/<author>/<qna_pk>/', views.qna_edit, name='qna_edit'),
	path('imageDelete/', views.image_delete, name='image_delete'),
	re_path(r'^(?P<pk>\d+)/$', views.view_qna, name='view_qna'),
	re_path(r'^(?P<pk>\d+)/(?P<comment_pk>\d+)/$', views.view_qna, name='view_qna_withcomment'),
	re_path(r'^(?P<pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/edit_ajax/$', views.comment_edit_ajax, name='comment_edit_ajax'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/delete_ajax/$', views.comment_delete_ajax, name='comment_delete_ajax')
	
]	
