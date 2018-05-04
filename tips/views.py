from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.db.models import Avg, F, Max, Min, Window
from django.http import JsonResponse
from django.utils.text import slugify
from django.utils.html import strip_tags
from accounts.models import UserProfile
from allauth.socialaccount.models import SocialAccount
from .models import Listicle, Comment, Article, Image
from .forms import CommentForm, ListicleForm, ArticleForm
import json

def subway(request):
	args = { 'gallery' : Article.objects.filter(category='subway' or 'Subway') }
	return render(request, 'tips/subway.html' , args)

def view_tips(request, pk, comment_pk=None):
	article = Article.objects.get(id=pk)
	article.views += 1
	article.save()
	authenticated_user = ''
	socialaccount = None
	if request.user.is_authenticated:
		authenticated_user = UserProfile.objects.get(user=request.user)
		try :
			socialaccount = SocialAccount.objects.get(user=request.user)
		except :
			socialaccount = None
	category = article.category
	form = CommentForm(request.POST, request.FILES)
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = CommentForm(request.POST, request.FILES)
			if form.is_valid():
				comment = form.save(commit=False)
				comment.article = Article.objects.get(pk=pk)
				comment.author = request.user
				try:
					parent = Comment.objects.get(pk=comment.parent)
				except:
					parent = None
				if comment.parent is 0 and comment_pk is None:
					group_max = Comment.objects.aggregate(Max('group'))
					if group_max['group__max'] is None:
						comment.group = 1
					else:
						comment.group = group_max['group__max']+1
					comment.seq_in_group = 0
					comment.parent = None
				elif comment_pk:
					comment = Comment.objects.get(pk=comment_pk)
					form = CommentForm(request.POST, request.FILES, instance=comment)
					if form.is_valid():
						if parent:
							comment.parent_author = parent.parent_author
						else:
							comment.parent_author = 'deleted comment'
				else:
					comment.depth = parent.depth + 1
					comment.group = parent.group
					comment.parent_author = parent.author
					if parent.seq_in_group is 0:
						seq_num = Comment.objects.filter(group=parent.group).aggregate(Max('seq_in_group'))
						comment.seq_in_group = seq_num['seq_in_group__max'] + 1
					else:
						updates = Comment.objects.filter(group=parent.group, seq_in_group__gt=parent.seq_in_group)
						for instance in updates:
							print(instance.seq_in_group)
							instance.seq_in_group +=1
							instance.save()
						comment.seq_in_group = parent.seq_in_group + 1
				comment.save()
				return redirect('tips:view_tips', pk)
		else:
			form = CommentForm()
	else:
		form = CommentForm()
	args = { 'article' : Article.objects.filter(id=pk),
			 'category' : category,
			 'form': form,
			 'authenticated_user' : authenticated_user,
			 'socialaccount': socialaccount,
	}
	return render(request, 'tips/view_tip.html' , args)

def view_listicle(request, listicle_pk, pk=None, comment_pk=None):
	listicle = Listicle.objects.get(id=listicle_pk)
	for article in listicle.articles.all():
		article.views += 1
		article.save()
	authenticated_user = ''
	socialaccount = None
	if request.user.is_authenticated:
		authenticated_user = UserProfile.objects.get(user=request.user)
		try :
			socialaccount = SocialAccount.objects.get(user=request.user)
		except :
			socialaccount = None
	form = CommentForm(request.POST, request.FILES)
	articleNum = form['article'].value()
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = CommentForm(request.POST, request.FILES)
			if form.is_valid():
				comment = form.save(commit=False)
				comment.article = Article.objects.get(pk=articleNum)
				comment.author = request.user
				try:
					parent = Comment.objects.get(pk=comment.parent)
				except:
					parent = None
				if comment.parent is 0 and comment_pk is None:
					group_max = Comment.objects.aggregate(Max('group'))
					if group_max['group__max'] is None:
						comment.group = 1
					else:
						comment.group = group_max['group__max']+1
					comment.seq_in_group = 0
					comment.parent = None
				elif comment_pk:
					comment = Comment.objects.get(pk=comment_pk)
					form = CommentForm(request.POST, request.FILES, instance=comment)
					if form.is_valid():
						if parent:
							comment.parent_author = parent.parent_author
						else:
							comment.parent_author = 'deleted comment'
				else:
					comment.depth = parent.depth + 1
					comment.group = parent.group
					comment.parent_author = parent.author
					if parent.seq_in_group is 0:
						seq_num = Comment.objects.filter(group=parent.group).aggregate(Max('seq_in_group'))
						comment.seq_in_group = seq_num['seq_in_group__max'] + 1
					else:
						updates = Comment.objects.filter(group=parent.group, seq_in_group__gt=parent.seq_in_group)
						for instance in updates:
							print(instance.seq_in_group)
							instance.seq_in_group +=1
							instance.save()
						comment.seq_in_group = parent.seq_in_group + 1
				comment.save()
				return redirect('tips:view_listicle', listicle_pk)
		else:
			form = CommentForm()
	else:
		form = CommentForm()
	args = {
			'listicle': listicle,
			'form' : form,
			'authenticated_user' : authenticated_user,
			'socialaccount': socialaccount,
			}
	return render(request, 'tips/view_listicle.html', args)

def listicle_admin(request):
	res ={}
	if request.method == 'POST':
		pk = request.POST['pk']
		result = Article.objects.filter(category=pk)
		for i in range(len(result)):
			res.update({result[i].id : result[i].title})
	return JsonResponse(res, safe=False)

# @csrf_exempt
def likesUpdate(request):
	updated = False
	liked = False
	user = request.user
	if user.is_authenticated:
		if request.method == 'POST':
			pk = request.POST['pk']
			updates = Article.objects.get(id=pk)
			if user in updates.likes.all():
				liked = False
				updates.likes.remove(user)
			else:
				liked =True
				updates.likes.add(user)
			updated = True
			res = {
				"updated": updated,
				"liked": liked,
				"likes_counts": "Likes {}".format(updates.likes.count()),
			}
			return JsonResponse(res, safe=False)
			# return HttpResponse(res['result'])
		else:
			return HttpResponse('post_error')
	return HttpResponse('login_require')

def articleText_call(request):
	if request.method == 'POST':
		pk = request.POST['pk']
		views_counts = Article.objects.get(id=pk)
		views_counts.views += 1
		views_counts.save()
		article = Article.objects.get(id=pk)
		res =  { 
			"title" : article.title,
			"text" : article.text,
			"views_counts": "Views {}".format(article.views),
			}
		print(res['text'])
		return JsonResponse(res, safe=False)
		# return HttpResponse(json.dumps(res), content_type='application/json')
	else:
		return HttpResponse('post_error')


@login_required
def comment_new(request, pk):
	article = Article.objects.get(id=pk)
	category = article.category
	if request.method == 'POST':
		form = CommentForm(request.POST, request.FILES)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.article = Article.objects.get(pk=pk)
			comment.author = request.user
			group_max = Comment.objects.aggregate(Max('group'))
			if group_max['group__max'] is None:
				comment.group = 1
			else:
				comment.group = group_max['group__max']+1
			comment.seq_in_group = 0
			comment.parent = None
			comment.save()
			return redirect('tips:view_tips', pk)
	else:
		form = CommentForm()
	args = { 'article' : Article.objects.filter(id=pk),
			 'category' : category,
			 'form': form,
	}
	return render(request, 'tips/comment_form.html', args)


def comment_edit_ajax(request, post_pk, comment_pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			pk = request.POST['c_pk']
			comment = Comment.objects.get(id=pk)
			res = {
				"comment_parent": comment.parent,
				"comment_message": comment.message
			}
			return JsonResponse(res, safe=False)
			# return HttpResponse(res['result'])
		else:
			return HttpResponse('post_error')
	return HttpResponse('login_require')

def comment_delete_ajax(request, post_pk, comment_pk):
	if request.user.is_authenticated:
		if request.method == 'POST':
			pk = request.POST['c_pk']
			comment = Comment.objects.get(id=pk)
			print("comment.paretnm", comment.id)
			updates = Comment.objects.filter(parent=comment.id)
			for update in updates:
				update.parent_author = 'deleted comment'
				update.save()
			comment.delete()
			comment_count = Comment.objects.filter(article=post_pk).count()
			res = {
				"comment_count": comment_count,
				"comment_message": 'success',
			}
			return JsonResponse(res, safe=False)
		else:
			return HttpResponse('delete_error')
	return HttpResponse('login_require')

def comment_edit(request, post_pk, comment_pk):
	comment = Comment.objects.get(pk=comment_pk)
	if comment.author != request.user:
		return redirect(comment)

	if request.method == 'POST':
		form = CommentForm(request.POST, request.FILES, instance=comment)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = Article.objects.get(pk=post_pk)
			comment.author = request.user
			comment.save()
			return redirect(comment)
	else:
		form = CommentForm(instance=comment)
	return render(request, 'tips/comment_form.html', {
		'form': form,
		})

def comment_delete(request, post_pk, comment_pk):
	comment = Comment.objects.get(pk=comment_pk)
	if comment.author != request.user:
		return redirect(comment)

	if request.method == 'POST':
		comment.delete()
		return redirect(comment)

	return render(request, 'tips/comment_confirm_delete.html', {
		'comment': comment,
		})

def add_to_cart_ajax(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			user_id = request.POST['user_id']
			article_id = request.POST['article_id']
			user = UserProfile.objects.get(id=user_id)
			article = Article.objects.get(id=article_id)
			if article in user.article_cart.all():
				return HttpResponse(0)
			else:
				user.article_cart.add(article)
				return HttpResponse(1)
		else:
			return HttpResponse(4) #post error
	else:
		return HttpResponse(5) #login require

def user_write_tip(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = ArticleForm(request.POST, request.FILES)
			if form.is_valid():
				article = form.save(commit=False)
				text = strip_tags(request.POST['text'])
				slug = slugify(text, allow_unicode=True)
				slug = slug.replace('nbsp', '-')
				max_length = 48
				if len(slug) <= max_length:
				    article.slug = slug
				trimmed_slug = slug[:max_length].rsplit('-', 1)[0]
				if len(trimmed_slug) <= max_length:
				    article.slug = trimmed_slug
				article.slug = slug[:max_length]+'...'
				article.author = request.user				
				article.save()
				return redirect(article)
		else:
			return redirect('home')
		form = ArticleForm()
	else:
		return redirect('home')

def title_check_ajax(request, article_pk=None):
	if request.user.is_authenticated:
		if request.method == "POST":
			title = request.POST['title']
			try :
				article = Article.objects.get(title=title)
				res = 1
			except:
				res = 0
			return HttpResponse(res)
		else:
			return HttpResponse(4) #post error
	else:
		return HttpResponse(5) #login require

def article_remove(request, author, article_pk):
	article = Article.objects.get(id=article_pk)
	if request.user.is_authenticated and article.author == request.user:
		article.delete()
		return redirect('home')
	else:
		return redirect("tips:view_tips", article_pk )

def article_edit(request, author, article_pk):
	article = Article.objects.get(id=article_pk)
	if request.method != 'POST' and request.user.is_authenticated and article.author == request.user:
		form = ArticleForm(instance=article)
		return render(request, 'tips/article_user_edit.html', {
			'form': form,
		})
	if request.method == 'POST' :
		form = ArticleForm(request.POST, request.FILES, instance=article)
		if form.is_valid():
			article = form.save(commit=False)
			text = strip_tags(request.POST['text'])
			slug = slugify(text, allow_unicode=True)
			slug = slug.replace('nbsp', '-')
			max_length = 48
			if len(slug) <= max_length:
			    article.slug = slug
			trimmed_slug = slug[:max_length].rsplit('-', 1)[0]
			if len(trimmed_slug) <= max_length:
			    article.slug = trimmed_slug
			article.slug = slug[:max_length]+'...'
			article.author = request.user				
			article.save()
			return redirect(article)		
	else:
		return redirect("tips:view_tips", article_pk)