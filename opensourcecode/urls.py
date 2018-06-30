"""opensourcecode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import  TemplateView
from django.views.generic.edit import     CreateView, UpdateView
from django.contrib.auth.views import login,logout
from django.contrib.auth.forms import   UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from dblog.views import  index 


urlpatterns = [ 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',  index , name='index' ), 
    url(r'^dblog/', include('dblog.urls')),    
     url(r'^login$', login,name='login'),
    url(r'^logout$', logout, name='logout'),    
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^socialprofile/', include('socialprofile.urls')),
    url(r'^summernote/', include('django_summernote.urls')), 
     
 ]  
