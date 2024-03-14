"""Ephemeral_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from Ephemeral_Backend.views import login_view, create_user_table, test_view
from Ephemeral_Backend.creationViews import create_user, test_body

urlpatterns = [
    path('test/', test_view),
    path('testBody/', test_body),
    path('login/<str:ephemeral_id>/<str:password>/', login_view, name='login'),
    path('createTable/', create_user_table, name='create_table'),
    path('createUser/', create_user)
]
