from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
from tips.models import Category, Image
from urllib import parse
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
	# p_page = request.META['HTTP_REFERER']
	p_page = parse.urlparse(request.META.get('HTTP_REFERER')).path
	args = {'p_page' : p_page,
			'subways' : Category.objects.filter(category='subway' or 'Subway'),
			'taxis' : Category.objects.filter(category='taxi' or 'Taxi'),
	 }
	return render(request, 'home.html', args)