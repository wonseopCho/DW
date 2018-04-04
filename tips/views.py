from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

from django.http import JsonResponse
from .models import Comment, Article, Image
from .forms import CommentForm
import json

def subway(request):
	args = { 'gallery' : Article.objects.filter(category='subway' or 'Subway') }
	return render(request, 'tips/subway.html' , args)

def view_tips(request, pk):
	article = Article.objects.get(id=pk)
	article.views += 1
	article.save()
	category = article.category
	args = { 'article' : Article.objects.filter(id=pk),
			 'category' : category,
	}
	return render(request, 'tips/view_tip.html' , args)

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
	if request.method == 'POST':
		form = CommentForm(request.POST, request.FILES)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.article = Article.objects.get(pk=pk)
			comment.author = request.user
			comment.save()
			return redirect('tips:view_tips', pk)
	else:
		form = CommentForm()
	return render(request, 'tips/comment_form.html', {
		'form': form,
		})

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