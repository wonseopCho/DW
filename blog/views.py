from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import models
#from django.http import HttpResponse



class PostLV(ListView):
	model = models.Post
	# template_name ='blog/post_list2.html' <== use own name
	# context_object_name ='posts' <== use own name
	paginate_by = 2

class PostDV(DetailView):
	model = models.Post

'''
def index(request):
	return render(request, 'blog/post_list.html', {
		'post_list': Post.objects.all(),
	})
#	return HttpResponse('hello JB blog view')


def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	return render(request, 'blog/post_detail.html', {
		'post': post,
	})

def post_year_archive(request, year):
	qs =Post.objects.filter(updated_at_year=year)
	return render(request,'blog/post_year_archive.html', {

	} )

def post_month_archive(request, year, month):
	qs =Post.objects.filter(updated_at_year=year, updated_at_month=month)
	return render(request,'blog/post_month_archive.html', {
		
	} )

def post_archive(request, year=None, month=None, day=None):
	qs = Post.objects.all()
	conditions = {}
	if year:
		conditions['updated_at_year'] = year
	if month:
		conditions['updated_at_month'] = month
	if day:
		conditions['upodated_at_dat'] = day
	qs = qs.filter(**conditions)
	return render(request,'blog/post_archive.html', {

	})
'''