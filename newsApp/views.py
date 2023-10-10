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
    """
    Handles user login functionality.

    If the request method is POST, attempts to authenticate the user.
    If authentication is successful, redirects the user to the home page.
    If authentication fails, displays an error message and stays on the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the home page upon successful login or stays on the login page if authentication fails.
    """
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
    """
    Handles user registration functionality.

    If the request method is POST, attempts to create a new user.
    If the username already exists, displays an error message and stays on the registration page.
    If registration is successful, redirects the user to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the login page upon successful registration or stays on the registration page if username already exists.
    """
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
    """
    Handles user logout functionality.

    Logs out the authenticated user and redirects them to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the login page after successful logout.
    """
    logout(request)
    messages.success(request,"You have been logged out successfully.")
    return redirect('login')

@login_required(login_url='login')
def HomePage(request):
    """
    Renders the home page with top headlines.

    Retrieves top headlines from the News API and displays them on the home page.
    Requires user authentication.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the home page template with top headlines.
    """
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
    """
    Handles news search functionality.

    Retrieves news articles based on user search query and category.
    Caches search results and displays them with optional sorting.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the search results page with news articles based on the user's search query.
    """
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
    """
    Displays user's saved search results.

    Retrieves and displays the user's saved search results from the cache.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the user searches page with saved search results.
    """
    context={}
    UserSearchData = CacheSearchResult.objects.filter(user=request.user)
    data = {x.keyword:GetCachedSearchresults(x.keyword) for x in UserSearchData}
    context['userSearches']=data
    return render(request,'news/user_searches.html',context)

def CacheSearchResults(keyword, user, search_result):
    """
    Caches search results and stores them in the database.

    Caches the provided search results using Django's cache mechanism and
    stores the results along with the search keyword and user in the database.

    Args:
        keyword (str): The search keyword used by the user.
        user (User): The authenticated user object.
        search_result (list): List of news articles to be cached.

    Returns:
        None
    """
    print(keyword)
    cache_key = f"search_results:{keyword}"
    cache.set(cache_key, search_result,timeout=3600)
    CacheSearchResult.objects.create(keyword=keyword,user=user,search_result=search_result)

def GetCachedSearchresults(keyword):
    """
    Retrieves cached search results from the cache.

    Retrieves the cached search results for the given keyword from Django's cache.

    Args:
        keyword (str): The search keyword used by the user.

    Returns:
        list or bool: List of cached news articles if found, False otherwise.
    """
    cache_key = f"search_results:{keyword}"
    search_result = cache.get(cache_key)
    if search_result is None:
        return False
    return search_result