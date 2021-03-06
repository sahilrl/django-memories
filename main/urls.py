"""memories URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login_facebook/', views.login_facebook, name='login_facebook'),
    path('login/', views.login_normal, name='login'),
    path('register/', views.signup, name='signup'),
    # path('accounts/', include('django.contrib.auth.urls')), # new
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('reset/', views.forget_password, name='reset'),
    path('reset-password/<uidb64>/<token>', views.setnewpass, name='setnewpass'),
]
