"""blog URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from django.conf.urls.static import static
from blog import settings
from authentication import views
from django.urls import path


urlpatterns = [
    path('admin/', views.admin, name = 'admin'),
    path('user/', views.user , name = 'user'),
    path('accounts/' , include('django.contrib.auth.urls')),
    path('signup/', views.signup , name = 'signup'),
    path('block/<num>', views.block, name = 'block'), 
    path('mkAdmin/<num>', views.adminMake, name = 'admin'), 
    path('adminManage/', views.adminManage, name='adminManage'),
    url(r'^', include('posts.urls')),
    url(r'^posts/', include('posts.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()