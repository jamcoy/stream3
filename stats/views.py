from django.shortcuts import render


def stats(request):
    return render(request, 'stats/stats.html')
