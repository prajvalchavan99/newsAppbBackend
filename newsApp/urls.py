from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('<str:keyword>', views.SearchNews,name="news"),
    path('', views.HomePage,name="home"),
]
