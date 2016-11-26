from django.shortcuts import render


def cars(request):
    return render(request, 'cars/cars.html')


def add_car(request):
    return render(request, 'cars/add_car.html')
