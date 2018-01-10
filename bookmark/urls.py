from django.contrib import admin
from django.urls import path
from . import views

app_name ='boomark'
urlpatterns = [
	path('', views.bookmark_list, name='BookmarkLV'),
	path('<int:id>/', views.bookmark_detail, name='BookmarkDV')
]

'''
*old_version using regular expression
url(r'^(?P<pk>\d+)/$', views.bookmark_detail, name='BookmarkDV')
-need to import next line as well
from django.conf.urls import url
'''
