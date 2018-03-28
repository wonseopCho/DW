from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Image

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
	res = {}
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
				"updated": updates,
				"liked": liked,
				"result": "Likes {}".format(updates.likes.count()),
			}
			return HttpResponse(res['result'])
		else:
			# return redirect('mapAPI:mapShow')
			return HttpResponse('post_error')
	return HttpResponse('login_require')

def test(request):
	return render(request, 'tips/test.html')