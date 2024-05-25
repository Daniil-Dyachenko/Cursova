from django.shortcuts import render


def create_customs(request):
    return render(request, 'customs/create_custom.html')
