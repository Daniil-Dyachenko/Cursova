from django.shortcuts import render
from django.http import HttpResponse

from sushi.models import Categories

# Create your views here.

def index(request):

    context = {
        'title': 'Sushi-bar - Головна',
        'content' : 'Суші-бар Акамедзутсу',
    }
    return render(request,'main/index.html',context )

def about(request):
    context = {
        'title': 'Sushi-bar - О нас',
        'content': 'О нас',
        "text_on_page": "Текст о магазине"
    }
    return render(request, 'main/about.html', context)
