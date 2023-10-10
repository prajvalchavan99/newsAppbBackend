import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.core.cache import cache
from .models import *
from django.contrib.auth import login,authenticate,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

@csrf_exempt
def UserLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password. Please try again.')
            return render(request,"auth/login.html")
    return render(request,"auth/login.html")

def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists. Please choose a different username.")
            return render(request, 'auth/register.html')
        user = User.objects.create_user(username=username, password=password)
        messages.success(request,"Registration successful. You can now log in.")
        return redirect('login')

    return render(request, 'auth/register.html')

def LogoutUser(request):
    logout(request)
    messages.success(request,"You have been logged out successfully.")
    return redirect('login')

@login_required(login_url='login')
def HomePage(request):
    context={}
    url =  settings.BASE_API_URL + "top-headlines?country=us"
    params = {
        'apiKey': settings.NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
    else:
        return JsonResponse({'error': response.text()}, status=500)
    context['newsData'] = data['articles']
    return render(request,'news/home_page.html',context)

@login_required(login_url='login')
def SearchNews(request):
    context={}
    if 'search' in request.GET:
        searchQuery = request.GET.get('search')
        category = request.GET.get('category')
        sortingOrder = request.GET.get('order')
        url =  settings.BASE_API_URL + "everything" if not category else settings.BASE_API_URL + "top-headlines"
        params = {
            'apiKey': settings.NEWS_API_KEY,
            'q': searchQuery,
            'page': 1
        }
        if category:
            params['category']=category
        response = requests.get(url, params=params)
        data = response.json()
        if data and len(data['articles'])>0:
            dataToBeStored=data['articles'][:3]
            CacheSearchResults(keyword=searchQuery,user=request.user,search_result=dataToBeStored)
            sortingOrder = True if  sortingOrder and '-' in sortingOrder else False
            context['newsData'] = sorted(data['articles'], key=lambda x: x['publishedAt'], reverse=sortingOrder)[:12]
        else:
            context['noDataForSearch']=f"No data for {searchQuery} in {category} category"
    return render(request,'news/search_news.html',context)


def UserSearches(request):
    context={}
    UserSearchData = CacheSearchResult.objects.filter(user=request.user)
    data = {x.keyword:GetCachedSearchresults(x.keyword) for x in UserSearchData}
    context['userSearches']=data
    return render(request,'news/user_searches.html',context)

def CacheSearchResults(keyword, user, search_result):
    print(keyword)
    cache_key = f"search_results:{keyword}"
    cache.set(cache_key, search_result,timeout=3600)
    CacheSearchResult.objects.create(keyword=keyword,user=user,search_result=search_result)

def GetCachedSearchresults(keyword):
    cache_key = f"search_results:{keyword}"
    search_result = cache.get(cache_key)
    if search_result is None:
        return False
    return search_result