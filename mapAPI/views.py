from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
from accounts.models import UserProfile
from allauth.socialaccount.models import SocialAccount
from tips.models import Category
from .models import MapAddress
import json

def mapShow(request):
	values = MapAddress.objects.values('lat', 'lng', 'type')
	markers = []
	authenticated_user = ''
	socialaccount = None
	if request.user.is_authenticated:
		authenticated_user = UserProfile.objects.get(user=request.user)
		try :
			socialaccount = SocialAccount.objects.get(user=request.user)
		except :
			socialaccount = None
	if len(values) != 0:
		for i in range(len(values)):
			if values[i]['type'] == 'restaurant': values[i]['type'] = 'R'
			elif values[i]['type'] == 'bar': values[i]['type'] = 'B'
			markers.append({'coord': {'lat':values[i]['lat'], 'lng':values[i]['lng']}, 'label':values[i]['type']})

	return render(request, 'mapAPI/map_show.html',{
		'map_api' : MapAddress.objects.all(),
		#'testJson' : json.dumps(serialize('json', MapAddress.objects.all(), cls=LazyEncoder)),
		'addresses' : json.dumps(serialize('json', MapAddress.objects.all())),
		'markers' : markers,
		'Google_key': settings.GOOGLE_API_KEY,
		'authenticated_user' : authenticated_user,
		'socialaccount': socialaccount,
		'categories' : Category.objects.all(),
	})

#@csrf_exempt
def latlngUpdates(request):
	if request.method == 'POST':
		lat = request.POST['lat']
		lng = request.POST['lng']
		id = request.POST['id']
		MapAddress.objects.filter(id=id).update(lat=lat, lng=lng)
		res = "{0}_updated".format(id)
		return HttpResponse(res)
	else:
		return redirect('mapAPI:mapShow')
	return render(request, 'mapAPI/map_Show.html')
