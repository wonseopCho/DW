from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
from tips.models import Category, Image
import json

#CVB
# class HomeView(TemplateView):
# 	template_name ='home.html'

# home_view = HomeView.as_view()

#FBV
'''
def home_view(request):
	return render(request, 'home.html')
'''

def home_view(request):
	args = { 'subways' : Category.objects.filter(category='subway' or 'Subway'),
			 'taxis' : Category.objects.filter(category='taxi' or 'Taxi')
	 }
	return render(request, 'home.html', args)