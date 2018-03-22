from django.contrib import admin
from django.urls import path
from . import views

app_name ='tips'
urlpatterns = [
	path('subway/', views.subway, name='subway'),
	path('subway/<pk>/', views.subway, name='subway'),
	
]
