import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

def SearchNews(request, keyword):
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': keyword,
        'apiKey': settings.NEWS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to fetch news articles'}, status=500)

def HomePage(request):
    context={}
    searchQuery = request.GET.get('search')
    sortingOrder = request.GET.get('order')
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


def SearchNews(request):
    context={}
    searchQuery = request.GET.get('search')
    url =  settings.BASE_API_URL + "everything"
    params = {
        'apiKey': settings.NEWS_API_KEY,
        'q': searchQuery,
        'page': 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    context['newsData'] = sorted(data['articles'], key=lambda x: x['publishedAt'], reverse=True)[:12]
    return render(request,'news/search_news.html',context)
