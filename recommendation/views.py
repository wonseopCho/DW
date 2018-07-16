from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, F, Max, Min, Window
from django.http import JsonResponse
from accounts.models import UserProfile
from allauth.socialaccount.models import SocialAccount
from tips.models import Category
from recommendation.models import Recommendation, Image 
from .models import Comment
from .forms import CommentForm
# Create your views here.


def view_recommendation(request, pk, comment_pk=None):
	recommendation = Recommendation.objects.get(id=pk)
	recommendation.views += 1
	recommendation.save()
	authenticated_user = ''
	socialaccount = None
	form = CommentForm(request.POST, request.FILES)
	if request.user.is_authenticated:
		authenticated_user = UserProfile.objects.get(user=request.user)
		try :
			socialaccount = SocialAccount.objects.get(user=request.user)
		except :
			socialaccount = None
	category = recommendation.category
	form = CommentForm(request.POST, request.FILES)
	if request.user.is_authenticated:
		user = UserProfile.objects.get(user=request.user)
		if request.method == 'POST':
			form = CommentForm(request.POST, request.FILES)
			if form.is_valid():
				print("yes")
				comment = form.save(commit=False)
				comment.recommendation = Recommendation.objects.get(pk=pk)
				comment.author = user.user
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
				return redirect('recommendation:view_recommendation', pk)
			else:
				print("Not valid")
		else:
			form = CommentForm()
	else:
		form = CommentForm()
	args = { 'article' : Recommendation.objects.filter(id=pk),
			 'category' : category,
			 'form': form,
			 'authenticated_user' : authenticated_user,
			 'socialaccount': socialaccount,
			 'categories' : Category.objects.all(),
			 'excludeArticles' : Recommendation.objects.filter(category=category).exclude(id=pk),
	}
	return render(request, 'recommendation/view_recommendation.html', args)


def likesUpdate(request):
	updated = False
	liked = False
	user = request.user
	if user.is_authenticated:
		if request.method == 'POST':
			pk = request.POST['pk']
			updates = Recommendation.objects.get(id=pk)
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

@login_required
def comment_new(request, pk):
	recommendation = Recommendation.objects.get(id=pk)
	category = recommendation.category
	if request.method == 'POST':
		form = CommentForm(request.POST, request.FILES)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.recommendation = Recommendation.objects.get(pk=pk)
			comment.author = request.user
			group_max = Comment.objects.aggregate(Max('group'))
			if group_max['group__max'] is None:
				comment.group = 1
			else:
				comment.group = group_max['group__max']+1
			comment.seq_in_group = 0
			comment.parent = None
			comment.save()
			return redirect('recommendation:view_recommendation', pk)
	else:
		form = CommentForm()
	args = { 'recommendation' : Recommendation.objects.filter(id=pk),
			 'category' : category,
			 'form': form,
	}
	return render(request, 'recommendation/comment_form.html', args)


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
			comment_count = Comment.objects.filter(recommendation=post_pk).count()
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
			comment.post = Recommendation.objects.get(pk=post_pk)
			comment.author = request.user
			comment.save()
			return redirect(comment)
	else:
		form = CommentForm(instance=comment)
	return render(request, 'recommendation/comment_form.html', {
		'form': form,
		})

def add_to_cart_ajax(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			user_id = request.POST['user_id']
			article_id = request.POST['article_id']
			user = UserProfile.objects.get(id=user_id)
			recommendation = Recommendation.objects.get(id=article_id)
			if recommendation in user.recommendation_cart.all():
				return HttpResponse(0)
			else:
				user.recommendation_cart.add(recommendation)
				return HttpResponse(1)
		else:
			return HttpResponse(4) #post error
	else:
		return HttpResponse(5) #login require