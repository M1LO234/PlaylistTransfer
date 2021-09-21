from django.urls import path, include
from myapi import views

urlpatterns = [
  path('', views.index, name='index')
]