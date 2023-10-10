from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # Authentication
    path('login/',views.UserLogin,name="login"),
    path('register/',views.Register,name="register"),
    path('logout/',views.LogoutUser,name="logout"),

    # News
    path('', views.HomePage,name="home"),
    path('search-news/', views.SearchNews,name="searchresults"),
    path('my-searches/',views.UserSearches,name="usersearches")
]
