from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.db.models import Avg, F, Max, Min, Window
from django.http import JsonResponse
from .models import Listicle, Comment, Article, Image
from .forms import CommentForm, ListicleForm
import json

def subway(request):
	args = { 'gallery' : Article.objects.filter(category='subway' or 'Subway') }
	return render(request, 'tips/subway.html' , args)

def view_tips(request, pk):
	article = Article.objects.get(id=pk)
	article.views += 1
	article.save()
	category = article.category
	form = CommentForm(request.POST, request.FILES)
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = CommentForm(request.POST, request.FILES)
			if form.is_valid():
				comment = form.save(commit=False)
				comment.article = Article.objects.get(pk=pk)
				comment.author = request.user
				if comment.parent != 0:
					parent = Comment.objects.get(pk=comment.parent)
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
				else:
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
	else:
		form = CommentForm()
	args = { 'article' : Article.objects.filter(id=pk),
			 'category' : category,
			 'form': form,
	}
	return render(request, 'tips/view_tip.html' , args)

def view_listicle(request, pk):
	listicle = Listicle.objects.get(id=pk)
	for article in listicle.articles.all():
		article.views += 1
		article.save()
	args = {'listicle': listicle}
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
			comment.save()
			return redirect('tips:view_tips', pk)
	else:
		form = CommentForm()
	args = { 'article' : Article.objects.filter(id=pk),
			 'category' : category,
			 'form': form,
	}
	return render(request, 'tips/comment_form.html', args)

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