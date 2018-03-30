from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.http import JsonResponse

from .models import Category, Image
import json

def subway(request):
	args = { 'gallery' : Category.objects.filter(category='subway' or 'Subway') }
	return render(request, 'tips/subway.html' , args)

def view_tip(request, pk):
	updates = Category.objects.get(id=pk)
	updates.views += 1
	updates.save()
	args = { 'tips' : Category.objects.filter(id=pk) }
	return render(request, 'tips/view_tip.html' , args)

# @csrf_exempt
def likesUpdate(request):
	updated = False
	liked = False
	user = request.user
	if user.is_authenticated:
		if request.method == 'POST':
			pk = request.POST['pk']
			updates = Category.objects.get(id=pk)
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
		views_counts = Category.objects.get(id=pk)
		views_counts.views += 1
		views_counts.save()
		article = Category.objects.get(id=pk)
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