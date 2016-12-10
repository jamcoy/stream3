from django.shortcuts import render


def index(request):
    return render(request, 'complementary_pages/index.html')


def about(request):
    return render(request, 'complementary_pages/about.html')


def contact(request):
    return render(request, 'complementary_pages/contact.html')


def terms(request):
    return render(request, 'complementary_pages/terms.html')
