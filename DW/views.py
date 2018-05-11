from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
from tips.models import Listicle, Category, Article, Image
from accounts.models import UserProfile
from allauth.socialaccount.models import SocialAccount
from urllib import parse
from tips.forms import ArticleForm
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
	socialaccount = None
	articleForm = ArticleForm()
	categories = Category.objects.all()
	if request.user.is_authenticated:
		authenticated_user = UserProfile.objects.get(user=request.user)
		try :
			socialaccount = SocialAccount.objects.get(user=request.user)
		except :
			socialaccount = None
	for cate in categories:
		category = Category.objects.get(category=cate.category).id
		category_articles.update({ cate.category : Article.objects.filter(category=category)})
		category_listicle.update({ cate.category : Listicle.objects.filter(category=category)})
	args.update({'category_articles' : category_articles,
				 'category_listicle' : category_listicle,
				 'authenticated_user' : authenticated_user,
				 'socialaccount': socialaccount,
				 'form' : articleForm,
				 'categories' : categories,
		})
	# print(args)
	return render(request, 'home.html', args)

@csrf_exempt
def service_worker_js(request):
	absAppPath = settings.BASE_DIR
	filename = '/service-worker.js'
	jsfile = open(absAppPath+filename, 'rb')
	response = HttpResponse(content=jsfile)
	response['Content-Type'] = 'text/javascript'
	response['Content-Disposition'] = 'attachment; filename="%s"'%(absAppPath+filename)
	return response