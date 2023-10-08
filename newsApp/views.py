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
    url =  settings.BASE_API_URL + "everything" if searchQuery else settings.BASE_API_URL + "top-headlines"
    params = {
        'apiKey': settings.NEWS_API_KEY
    }

    if searchQuery:
        params['q'] = searchQuery

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
    else:
        return JsonResponse({'error': response.text()}, status=500)
    # print(data)
    context['newsData'] = data
    return render(request,'news/home_page.html',context)

