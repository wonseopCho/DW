from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
from tips.models import Listicle, Category, Article, Image
from accounts.models import UserProfile
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
	args= {'p_page' : p_page}
	category_articles={}
	category_listicle={}
	authenticated_user = ''
	if request.user.is_authenticated:
		authenticated_user = UserProfile.objects.get(user=request.user)
	for cate in Category.objects.all():
		category = Category.objects.get(category=cate.category).id
		category_articles.update({ cate.category : Article.objects.filter(category=category)})
		category_listicle.update({ cate.category : Listicle.objects.filter(category=category)})
	args.update({'category_articles' : category_articles,
				 'category_listicle' : category_listicle,
				 'authenticated_user' : authenticated_user,
		})
	print(args)
	return render(request, 'home.html', args)