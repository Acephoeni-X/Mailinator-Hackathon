from django.contrib import admin
from django.urls import path, include
from appone import views


urlpatterns = [
    path('', views.front, name='front'),
    path('send', views.email, name='send'),
    path('form', views.index, name='form'),
]
