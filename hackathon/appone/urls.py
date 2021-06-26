from django.contrib import admin
from django.urls import path, include
from appone import views

urlpatterns = [
    path('form', views.index, name='form'),
]
