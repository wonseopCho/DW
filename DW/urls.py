"""DW URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve
from django.http import HttpResponse, HttpResponseNotFound
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout
from tips.models import Article, Category
from DW import views

def staticView(request):
    with open(settings.BASE_DIR+"/service-worker.js") as fp:
        return HttpResponse(fp.read())

args = {'categories' : Category.objects.all()}
urlpatterns = [
    # path('service-worker.js/', staticView),
    path('service-worker.js/', views.service_worker_js),
    path('', views.index_view, name='index'),
    path('home/', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('blog2/', include('blog2.urls')),
    path('bookmark/', include('bookmark.urls')),
    path('mapAPI/', include('mapAPI.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', login, {'template_name':'login.html', 'extra_context': args} ,name='login'),
    path('logout/', logout, {'template_name':'logout.html'}, name='logout'),
    path('tips/', include('tips.urls')),
    path('recommendation/', include('recommendation.urls')),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)