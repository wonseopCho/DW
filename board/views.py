from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, F, Max, Min, Window
from django.http import JsonResponse
from django.utils.text import slugify
from django.utils.html import strip_tags
from accounts.models import UserProfile
from allauth.socialaccount.models import SocialAccount
from tips.models import Category
from .models import Board, Image, Comment
from .forms import CommentForm, BoardForm
# Create your views here.


def view_board(request, pk, comment_pk=None):
	board = Board.objects.get(id=pk)
	board.views += 1
	board.save()
	authenticated_user = ''
	socialaccount = None
	form = CommentForm(request.POST, request.FILES)
	if request.user.is_authenticated:
		authenticated_user = UserProfile.objects.get(user=request.user)
		try :
			socialaccount = SocialAccount.objects.get(user=request.user)
		except :
			socialaccount = None
	form = CommentForm(request.POST, request.FILES)
	if request.user.is_authenticated:
		user = UserProfile.objects.get(user=request.user)
		if request.method == 'POST':
			form = CommentForm(request.POST, request.FILES)
			if form.is_valid():
				print("yes")
				comment = form.save(commit=False)
				comment.board = Board.objects.get(pk=pk)
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
				return redirect('board:view_board', pk)
			else:
				print("Not valid")
		else:
			form = CommentForm()
	else:
		form = CommentForm()
	args = { 'boards' : Board.objects.filter(id=pk),
			 'form': form,
			 'authenticated_user' : authenticated_user,
			 'socialaccount': socialaccount,
			 'categories' : Category.objects.all(),
			 'excludeQnas' : Board.objects.all().exclude(id=pk),
	}
	return render(request, 'board/view_board.html', args)


def likesUpdate(request):
	updated = False
	liked = False
	user = request.user
	if user.is_authenticated:
		if request.method == 'POST':
			pk = request.POST['pk']
			updates = Board.objects.get(id=pk)
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
				"likes_counts": "{}".format(updates.likes.count()),
			}
			return JsonResponse(res, safe=False)
			# return HttpResponse(res['result'])
		else:
			return HttpResponse('post_error')
	return HttpResponse('login_require')

def board_remove(request, author, board_pk):
	board = Board.objects.get(id=board_pk)
	if request.user.is_authenticated and board.author == request.user:
		board.delete()
		return redirect('home')
	else:
		return redirect("board:view_tips", board_pk )

@login_required
def comment_new(request, pk):
	board = Board.objects.get(id=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST, request.FILES)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.board = Board.objects.get(pk=pk)
			comment.author = request.user
			group_max = Comment.objects.aggregate(Max('group'))
			if group_max['group__max'] is None:
				comment.group = 1
			else:
				comment.group = group_max['group__max']+1
			comment.seq_in_group = 0
			comment.parent = None
			comment.save()
			return redirect('board:view_board', pk)
	else:
		form = CommentForm()
	args = { 'board' : Board.objects.filter(id=pk),
			 'form': form,
	}
	return render(request, 'board/comment_form.html', args)


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
			comment_count = Comment.objects.filter(board=post_pk).count()
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
			comment.post = Board.objects.get(pk=post_pk)
			comment.author = request.user
			comment.save()
			return redirect(comment)
	else:
		form = CommentForm(instance=comment)
	return render(request, 'board/comment_form.html', {
		'form': form,
		})

def add_to_cart_ajax(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			user_id = request.POST['user_id']
			board_id = request.POST['board_id']
			user = UserProfile.objects.get(id=user_id)
			board = Board.objects.get(id=board_id)
			if board in user.board_cart.all():
				return HttpResponse(0)
			else:
				user.board_cart.add(board)
				return HttpResponse(1)
		else:
			return HttpResponse(4) #post error
	else:
		return HttpResponse(5) #login require

def user_write_board(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = BoardForm(request.POST, request.FILES)
			if form.is_valid():
				board = form.save(commit=False)
				title = request.POST['b_title'] 
				text = strip_tags(request.POST['text'])
				slug = slugify(text, allow_unicode=True)
				slug = slug.replace('nbsp', '-')
				max_length = 48
				if len(slug) <= max_length:
				    board.slug = slug
				trimmed_slug = slug[:max_length].rsplit('-', 1)[0]
				if len(trimmed_slug) <= max_length:
				    board.slug = trimmed_slug
				board.slug = slug[:max_length]+'...'
				board.q_title = title
				board.author = request.user				
				board.save()
				return redirect(board)
		else:
			return redirect('home')
		form = BoardForm()
	else:
		return redirect('home')

def board_edit(request, author, board_pk):
	board = Board.objects.get(id=board_pk)
	authenticated_user = ''
	socialaccount = None
	if request.user.is_authenticated:
		authenticated_user = UserProfile.objects.get(user=request.user)
		try :
			socialaccount = SocialAccount.objects.get(user=request.user)
		except :
			socialaccount = None

	if request.method != 'POST' and request.user.is_authenticated and board.author == request.user:
		form = BoardForm(instance=board)
		return render(request, 'board/board_user_edit.html', {
			'form': form,
			'authenticated_user' : authenticated_user,
			'socialaccount': socialaccount,
			'categories' : Category.objects.all(),
		})

	if request.method == 'POST' :
		form = BoardForm(request.POST, request.FILES, instance=board)
		if form.is_valid():
			board = form.save(commit=False)
			rating = strip_tags(request.POST['rating'])
			text = strip_tags(request.POST['text'])
			slug = slugify(text, allow_unicode=True)
			slug = slug.replace('nbsp', '-')
			max_length = 48
			if len(slug) <= max_length:
			    board.slug = slug
			trimmed_slug = slug[:max_length].rsplit('-', 1)[0]
			if len(trimmed_slug) <= max_length:
			    board.slug = trimmed_slug
			board.slug = slug[:max_length]+'...'
			board.rating = rating
			board.author = request.user				
			board.save()
			return redirect(board)		
	else:
		return redirect("board:view_board", board_pk)

def image_delete(request):
	# print(Attachment.objects.all())
	if request.user.is_authenticated:
		if request.method == "POST":
			image_src = request.POST['file']
			try:
				instance = Attachment.objects.get(file=image_src)
			except:
				instance = False
			if instance is not False:
				try:
					instance.file.delete()
					instance.delete()
					return HttpResponse(1) # instance and file deleted from DB success
				except:
					return HttpResponse(2) # delete error
			else:
				return HttpResponse(3) # no instance exist
		return redirect('home') # POST error
	else:
		return redirect('accounts:account_login') #login require