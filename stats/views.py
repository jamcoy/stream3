from django.shortcuts import render
from cars.models import Car, Refuel
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


def select_sub_details(request):
    filters = {'exclude_from_collation': False,
               'make': request.GET.get('make', None),
               'model': request.GET.get('model', None),
               'year_of_manufacture': request.GET.get('year', None)
               }
    sub_model = request.GET.get('sub_model', None)
    if sub_model is not None and (sub_model != "[None]"):
        filters['sub_model'] = sub_model
    cylinder_capacity = request.GET.get('cylinder_capacity', None)
    if cylinder_capacity is not None and (cylinder_capacity != "[None]"):
        filters['cylinder_capacity'] = cylinder_capacity
    fuel_type = request.GET.get('fuel_type', None)
    if fuel_type is not None and (fuel_type != "[None]"):
        filters['fuel_type'] = fuel_type
    transmission = request.GET.get('transmission', None)
    if transmission is not None and (transmission != "[None]"):
        filters['transmission'] = transmission

    queries = []
    if sub_model is None or 'Select':
        queries.append(query_details_count('sub_model', filters))
    if cylinder_capacity is None or 'Select':
        queries.append(query_details_count('cylinder_capacity', filters))
    if fuel_type is None or 'Select':
        queries.append(query_details_count('fuel_type', filters))
    if transmission is None or 'Select':
        queries.append(query_details_count('transmission', filters))

    queries.append(calculate_economy(filters))

    return HttpResponse(json.dumps(queries), content_type='application/json')


def query_details_count(field, filters):  # not a view
    query = Car.objects.values(field).filter(**filters).annotate(n=Count("pk"))
    data_model = [{field: item[field], 'number': item['n']} for item in query]
    return data_model


def calculate_economy(filters):  # not a view
    all_cars = Car.objects.values().filter(**filters)

    return [{'cars_in_sample': len(all_cars),
             'distance': '3,345,234',
             'economy_calculation': '45.3 MPG'}]
