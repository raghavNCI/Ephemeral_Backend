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
from Ephemeral_Backend.Views.generalViews import login_view, create_user_table, test_view, get_user, create_peer_table, get_peers, create_displayPic_Bucket
from Ephemeral_Backend.Views.creationViews import create_user, add_peer, add_dp, test_body

urlpatterns = [
    path('', test_view),
    path('test/', test_view),
    path('testBody/', test_body),
    path('login/<str:ephemeral_id>/<str:password>/', login_view, name='login'),
    path('createUserTable/', create_user_table),
    path('createPeerTable/', create_peer_table),
    path('createUser/', create_user),
    path('searchUser/<str:eph_id>/', get_user),
    path('getPeers/<str:eph_id>/', get_peers),
    path('addPeer/<str:addTo>/<str:addId>/', add_peer),
    path('createDPBucket/', create_displayPic_Bucket),
    path('addDp/', add_dp)
]
