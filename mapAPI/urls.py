from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse, HttpResponseNotFound
from . import views


app_name = "mapAPI"
urlpatterns = [
	path('',views.mapShow, name= "mapShow"),
	path('latlngUpdates/', views.latlngUpdates, name='latlngUpdates')
]
