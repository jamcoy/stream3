from django.shortcuts import render, redirect, get_object_or_404
from urllib2 import urlopen
from .forms import PlateForm
import json
from django.contrib.auth.decorators import login_required
from .models import Car
from django.conf import settings
from django.core.urlresolvers import reverse


def list_cars(request):
    if Car.objects.filter(user_id=request.user):
        first_car = Car.objects.filter(user_id=request.user)[:1].get()
        return redirect(cars, first_car.pk)  # for the moment it redirects to user's 1st car
    else:  # if user has no cars, send them to the add car form
        form = PlateForm()
        return render(request, 'cars/add_car.html', {'form': form})


@login_required()
def cars(request, car_id):
    car_detail = get_object_or_404(Car, pk=car_id, user_id=request.user)
    cars = Car.objects.filter(user_id=request.user)
    return render(request, 'cars/cars.html', {'car_detail': car_detail, 'cars': cars})


@login_required()
def add_car(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlateForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            url = "https://dvlasearch.appspot.com/DvlaSearch?apikey=DvlaSearchDemoAccount&licencePlate="
            page = urlopen(url + form.cleaned_data['your_reg'])
            car_details = json.loads(page.read())
            car_details['yourReg'] = form.cleaned_data['your_reg']
            request.session['full_car_details'] = car_details
            check = True  # expand upon this!
            if check:
                return render(request, "cars/add_car_details.html", {'car_details': car_details})
            else:
                # generate an error
                pass

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlateForm()

    return render(request, 'cars/add_car.html', {'form': form})  # should this be indented?


@login_required()
def add_car_details(request):
    if request.method == 'POST':
        car_details = request.session['full_car_details']
        request.session['full_car_details'] = ""  # necessary to clear??
        # validation not required here - user cannot edit anything - just confirming right vehicle
        c = Car(user=request.user,
                make=car_details['make'],
                model=car_details['model'],
                colour=car_details['colour'],
                year_of_manufacture=car_details['yearOfManufacture'],
                cylinder_capacity=car_details['cylinderCapacity'],
                transmission=car_details['transmission'],
                fuel_type=car_details['fuelType'],
                co2=car_details['co2Emissions'],
                doors=car_details['numberOfDoors'],
                total_fuel_litres=0,
                total_fuel_expenditure=0,
                total_mileage_tracked=0,
                refuels=0)
        c.save()
        return redirect('/cars')  # add parameter to show new car
        # http: // stackoverflow.com / questions / 12671649 / redirect - to - index - page - after - submiting - form - in -django  # 12671778
        # http://stackoverflow.com/questions/40411012/best-practice-help-to-redirect-in-django-after-form-submit

    # if a GET (or any other method) we'll go back to the original form
    else:
        form = PlateForm()

    return render(request, 'cars/add_car.html', {'form': form})  # should this be indented?
