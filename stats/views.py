from django.shortcuts import render
from cars.models import Car
from django.db.models import Count
from django.http import HttpResponse
import json


def economy_stats(request):
    makes = Car.objects.values("make")\
                       .filter(exclude_from_collation=False)\
                       .annotate(n=Count("pk"))
    return render(request, 'stats/stats.html', {'makes': makes})


def select_model(request):
    make = request.GET.get('make', None)
    query_models = Car.objects.values("model")\
                              .filter(exclude_from_collation=False, make=make)\
                              .annotate(n=Count("pk"))
    data_models = [{'model': item['model'], 'number': item['n']} for item in query_models]
    return HttpResponse(json.dumps(data_models), content_type='application/json')


def select_year(request):
    make = request.GET.get('make', None)
    model = request.GET.get('model', None)
    query_years = Car.objects.values("year_of_manufacture")\
                             .filter(exclude_from_collation=False, make=make, model=model)\
                             .annotate(n=Count("pk"))
    data_models = [{'year': item['year_of_manufacture'], 'number': item['n']} for item in query_years]
    return HttpResponse(json.dumps(data_models), content_type='application/json')


def economy_apply_filters(request):
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
