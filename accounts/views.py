from django.shortcuts import render


def register(request):
    return render(request, 'www/index.html')


def login(request):
    return render(request, 'www/index.html')


def logout(request):
    return render(request, 'www/index.html')


def profile(request):
    return render(request, 'www/index.html')
