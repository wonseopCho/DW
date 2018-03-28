from django.contrib import admin
from django.urls import path,re_path
from django.http import HttpResponse, HttpResponseNotFound
from . import views

app_name ='tips'
urlpatterns = [
	path('subway/', views.subway, name='subway'),
	path('likesUpdate/', views.likesUpdate, name='likesUpdate'),
	path('test/', views.test, name='test'),
	re_path(r'^(?P<pk>\d+)/$', views.view_tip, name='view_tip'),
]	
