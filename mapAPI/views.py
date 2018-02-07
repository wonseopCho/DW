from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from .models import MapAddress
import json


# Create your views here.
'''
class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, 'json'):
            return str(obj)
        return super().default(obj)
'''
def mapShow(request):
	
	values = MapAddress.objects.values('lat', 'lng', 'type')
	markers = []
	if len(values) != 0:
		for i in range(len(values)):
			if values[i]['type'] == 'restaurant': values[i]['type'] = 'R'
			elif values[i]['type'] == 'bar': values[i]['type'] = 'B'
			markers.append({'coord': {'lat':values[i]['lat'], 'lng':values[i]['lng']}, 'label':values[i]['type']})

	return render(request, 'mapAPI/map_show.html',{
		'map_api' : MapAddress.objects.all(),
		#'testJson' : json.dumps(serialize('json', MapAddress.objects.all(), cls=LazyEncoder)),
		'addresses' : json.dumps(serialize('json', MapAddress.objects.all())),
		'markers' : json.dumps(markers),
	})

#@csrf_exempt
def latlngUpdates(request):
	if request.method == 'POST':
		data = request.POST['lat']
		res = "you sent a post request </b> <br> returned data: %s" % data
		return HttpResponse(res)
	return render(request)