from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import CommentForm

# Create your views here.
def index(request):
	return render(request, 'blog2/index.html', {
		'post_list' : Post.objects.all()
		})

def post_new(request):
	return render(request, 'blog2/post_new.html')

def post_detail(request, pk):
	return render(request, 'blog2/post_detail.html', {
		'post_detail' : Post.objects.get(pk=pk)
		})

def comment_new(request, pk):
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = Post.objects.get(pk=pk)
			comment.save()
			return redirect('blog2:detail', pk)
	else:
		form = CommentForm()
	return render(request, 'blog2/post_form.html', {
		'form': form,
		})

def comment_edit(request, post_pk, comment_pk):
	comment = Comment.objects.get(pk=comment_pk)
	if request.method == 'POST':
		form = CommentForm(request.POST, instance=comment)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = Post.objects.get(pk=post_pk)
			comment.save()
			return redirect('blog2:detail', post_pk)
	else:
		form = CommentForm(instance=comment)
	return render(request, 'blog2/post_form.html', {
		'form': form,
		})