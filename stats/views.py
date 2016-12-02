from django.shortcuts import render
from cars.models import Car
from django.db.models import Count
from django.http import HttpResponse


def test_ajax(request):
    make = request.GET.get('make', None)
    make += " received in view and passed back."
    return HttpResponse(make)


def economy_stats(request):
    makes = Car.objects.values("make").filter(exclude_from_collation=False).annotate(n=Count("pk"))
    return render(request, 'stats/stats.html', {'makes': makes})


def economy_stats_model(request, make):
    models = Car.objects.values("model").filter(exclude_from_collation=False, make=make).annotate(n=Count("pk"))
    return render(request, 'stats/stats.html', {'models': models})


def economy_stats_calculate(request, make, model, year, sub_model, engine, fuel, transmission):
    years = Car.objects.values("year_of_manufacture") \
                       .filter(exclude_from_collation=False, make=make, model=model, year=year) \
                       .annotate(n=Count("pk"))
    sub_models = Car.objects.values("sub_model") \
                            .filter(exclude_from_collation=False, make=make, model=model, year=year) \
                            .annotate(n=Count("pk"))
    engines = Car.objects.values("cylinder_capacity")\
                         .filter(exclude_from_collation=False, make=make, model=model, year=year)\
                         .annotate(n=Count("pk"))
    fuel_types = Car.objects.values("fuel_type")\
                            .filter(exclude_from_collation=False, make=make, model=model, year=year)\
                            .annotate(n=Count("pk"))
    transmissions = Car.objects.values("transmission") \
                      .filter(exclude_from_collation=False, make=make, model=model, year=year) \
                      .annotate(n=Count("pk"))
    filters = {'exclude_from_collation': False}
    if make:
        filters['make'] = make
    if model:
        filters['model'] = model
    if year:
        filters['year'] = year
    if sub_model:
        filters['sub_model'] = sub_model
    if engine:
        filters['engine'] = engine
    if fuel:
        filters['fuel'] = fuel
    if transmission:
        filters['transmission'] = transmission
    filtered_cars = Car.objects.filter(**filters)
    # calculate economy here
    return render(request, 'stats/stats.html', {'filtered': filtered_cars})
