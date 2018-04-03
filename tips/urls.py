from django.contrib import admin
from django.urls import path,re_path
from django.http import HttpResponse, HttpResponseNotFound
from . import views

app_name ='tips'
urlpatterns = [
	path('subway/', views.subway, name='subway'),
	path('likesUpdate/', views.likesUpdate, name='likesUpdate'),
	path('articleText_call/', views.articleText_call, name='articleText_call'),
	re_path(r'^subway/(?P<pk>\d+)/$', views.view_subway_tip, name='view_subway'),
	re_path(r'^taxi/(?P<pk>\d+)/$', views.view_taxi_tip, name='view_taxi'),
	re_path(r'^bus/(?P<pk>\d+)/$', views.view_bus_tip, name='view_bus'),
	re_path(r'^(?P<pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
	re_path(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
]	
