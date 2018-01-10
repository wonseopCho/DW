from django.shortcuts import render
from django.views.generic import TemplateView, View

#CVB
class HomeView(TemplateView):
	template_name ='home.html'

home_view = HomeView.as_view()

#FBV
'''
def home_view(request):
	return render(request, 'home.html')
'''