from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Image

def subway(request):
	args = { 'gallery' : Category.objects.filter(category='subway') }
	return render(request, 'tips/subway.html' , args)