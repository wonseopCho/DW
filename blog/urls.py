from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name ='blog'
urlpatterns = [
	path('', views.PostLV.as_view(), name='blogLV'),
	#path('post/<slug:slug>', views.PostDV.as_view(), name='postDV'),
	#re_path(r'^post/(?P<slug>[\.\,\?\-\!a-zA-Z0-9\ㄱ-ㅣ가-힣]+)/$', views.PostDV.as_view(), name='postDV'),
	re_path(r'^post/(?P<slug>[\.\,\?\-\!a-zA-Z0-9\u3131-\u3163\uac00-\ud7a3]+)/$', views.PostDV.as_view(), name='postDV'),
] 
