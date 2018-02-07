from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Bookmark
from django.http import JsonResponse
#from django.http import HttpResponse

#CBV
'''
class BookmarkLV(ListView):
	model = Bookmark

bookmark_list =  BookmarkLV.as_view()
'''

#FBV

def bookmark_list(request):
	return render(request, 'bookmark/bookmark_list.html', {
		'bookmark_list' : Bookmark.objects.all(),
	})


'''CBV
class BookmarkDV(DetailView):
	model =  Bookmark

bookmark_detail = BookmarkDV.as_view()
'''
#FBV
def bookmark_detail(request, id):
	bookmark = get_object_or_404(Bookmark, pk=id)
	return render(request, 'bookmark/bookmark_detail.html', {
		'bookmark': bookmark,
	})


'''
def bookmarkLV(request):
	return render(request, 'bookmark/bookmark_list.html')
'''
#	return HttpResponse('hello JB blog view')
	