from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from accounts.models import UserProfile
from tips.models import Listicle, Category, Article
from tips.forms import ArticleForm
from recommendation.models import Recommendation
from board.models import Board
from board.forms import BoardForm
from qna.models import Qna
from qna.forms import QnaForm
from urllib import parse
import json
import os
from el_pagination.decorators import page_template
#CVB
# class HomeView(TemplateView):
# 	template_name ='home.html'

# home_view = HomeView.as_view()

#FBV
'''
def home_view(request):
	return render(request, 'home.html')
'''

def index_view(request):
	p_page = parse.urlparse(request.META.get('HTTP_REFERER')).path
	args= {'p_page' : p_page}
	category_articles={}
	category_listicle={}
	category_user_articles={}
	category_recommendation={}
	authenticated_user = ''
	socialaccount = None
	if request.user.is_authenticated:
		authenticated_user = UserProfile.objects.get(user=request.user)
		try :
			socialaccount = SocialAccount.objects.get(user=request.user)
		except :
			socialaccount = None
	categories = Category.objects.all().order_by('id')
	for cate in categories:
		category = Category.objects.get(category=cate.category).id
		category_listicle.update({ cate.category : Listicle.objects.filter(category=category)})
		category_articles.update({ cate.category : Article.objects.filter(author__in=User.objects.filter(is_staff=1),).filter(category=category).order_by('-id')[:6]})
		category_user_articles.update({ cate.category : Article.objects.filter(author__in=User.objects.filter(is_staff=0),).filter(category=category).order_by('-id')})
		category_recommendation.update({ cate.category : Recommendation.objects.filter(category=category)})
	args.update({
				 'listicle_all' : Listicle.objects.all,
				 'category_listicle' : category_listicle,
				 'category_articles' : category_articles,
				 'category_user_articles' : category_user_articles,
				 'category_recommendation' : category_recommendation,
				 'authenticated_user' : authenticated_user,
				 'socialaccount': socialaccount,
				 'categories' : categories,
		})
	return render(request, 'index.html', args)


# @page_template('home_pagenation.html')
def home_view(request):
	# p_page = request.META['HTTP_REFERER']
	template='home.html'
	page_template = "home_pagenation.html"
	p_page = parse.urlparse(request.META.get('HTTP_REFERER')).path
	args= {'p_page' : p_page}
	category_articles={}
	category_listicle={}
	category_user_articles={}
	category_recommendation={}
	authenticated_user = ''
	socialaccount = None
	articleForm = ArticleForm()
	qnaForm = QnaForm()
	categories = Category.objects.all()
	if request.user.is_authenticated:
		authenticated_user = UserProfile.objects.get(user=request.user)
		try :
			socialaccount = SocialAccount.objects.get(user=request.user)
		except :
			socialaccount = None
	for cate in categories:
		category = Category.objects.get(category=cate.category).id
		category_listicle.update({ cate.category : Listicle.objects.filter(category=category)})
		articles = Article.objects.filter(author__in=User.objects.filter(is_staff=1),).filter(category=category).order_by('-id')
		# paginator = Paginator(articles,5)
		# page = request.GET.get('page')
		# page_articles = paginator.get_page(page)
		# category_articles.update({ cate.category : page_articles})
		category_articles.update({ cate.category : articles})
		category_user_articles.update({ cate.category : Article.objects.filter(author__in=User.objects.filter(is_staff=0),).filter(category=category).order_by('-id')})
		category_recommendation.update({ cate.category : Recommendation.objects.filter(category=category)})
	args.update({'category_listicle' : category_listicle,
				 'category_articles' : category_articles,
				 'category_user_articles' : category_user_articles,
				 'category_recommendation' : category_recommendation,
				 'authenticated_user' : authenticated_user,
				 'socialaccount': socialaccount,
				 'form' : articleForm,
				 'boardform' : BoardForm,
				 'qnaform' : QnaForm,
				 'categories' : categories,
				 'boards' : Board.objects.all().order_by('-id'),
				 'qnas' : Qna.objects.all().order_by('-id'),
		})
	# if extra_context is not None:
	# 	args.update(extra_context)
	if request.is_ajax():
		template = page_template
	return render(request, template, args)

@csrf_exempt
def service_worker_js(request):
	absAppPath = settings.BASE_DIR
	filename = '/service-worker.js'
	jsfile = open(absAppPath+filename, 'rb')
	response = HttpResponse(content=jsfile)
	response['Content-Type'] = 'text/javascript'
	response['Content-Disposition'] = 'attachment; filename="%s"'%(absAppPath+filename)
	return response
