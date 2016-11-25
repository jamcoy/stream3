from django.shortcuts import render


def index(request):
    return render(request, 'www/index.html')


def about(request):
    return render(request, 'www/about.html')


def contact(request):
    return render(request, 'www/contact.html')


def terms(request):
    return render(request, 'www/terms.html')
