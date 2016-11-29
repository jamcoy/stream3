from django.shortcuts import render, redirect, get_object_or_404
from urllib2 import urlopen
from .forms import PlateForm, RefuelForm
import json
from django.contrib.auth.decorators import login_required
from .models import Car
from django.contrib import messages


@login_required()
def list_cars(request):
    if Car.objects.filter(user_id=request.user):
        first_car = Car.objects.filter(user_id=request.user)[:1].get()
        return redirect(cars, first_car.pk)  # for the moment it redirects to user's 1st car
    else:  # if user has no cars, send them to the add car form
        form = PlateForm()
        return render(request, 'cars/add_car.html', {'form': form})  # maybe shouldn't be indented


@login_required()
def cars(request, car_id):
    car_detail = get_object_or_404(Car, pk=car_id, user_id=request.user)
    cars_list = Car.objects.filter(user_id=request.user)
    return render(request, 'cars/cars.html', {'car_detail': car_detail, 'cars_list': cars_list})


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
            check = True  # expand upon this (checking what comes back from API)
            if check:
                return render(request, "cars/add_car_details.html", {'car_details': car_details})
            else:
                # generate an error
                pass
    else:  # if a GET (or any other method) we'll create a blank form
        form = PlateForm()
        return render(request, 'cars/add_car.html', {'form': form})  # maybe shouldn't be indented


@login_required()
def add_car_details(request):
    if request.method == 'POST':
        car_details = request.session['full_car_details']
        request.session['full_car_details'] = ""  # necessary to clear??
        # validation not required here - user cannot edit anything - just confirming right vehicle
        # total_mileage and previous_mileage deliberately omitted
        # the car owner will never see the model / sub_model split, but it will be used when browsing mpg data
        model = car_details['model'].split(' ', 1)[0]
        sub_model = car_details['model'].split(' ', 1)[1]
        c = Car(user=request.user,
                make=car_details['make'],
                model=model,
                sub_model=sub_model,
                colour=car_details['colour'],
                year_of_manufacture=car_details['yearOfManufacture'],
                cylinder_capacity=car_details['cylinderCapacity'],
                transmission=car_details['transmission'],
                fuel_type=car_details['fuelType'],
                co2=car_details['co2Emissions'],
                doors=car_details['numberOfDoors'])
        c.save()
        latest_car = Car.objects.latest('date_added')  # django is asynchronous, so save() has completed
        return redirect(cars, latest_car.pk)
    else:
        form = PlateForm()
        return render(request, 'cars/add_car.html', {'form': form})  # maybe shouldn't be indented


@login_required()
def delete_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id, user_id=request.user)
    if request.method == 'POST':  # user has confirmed deleting car
        car.delete()
        messages.success(request, "Your car was deleted!")
        return redirect(list_cars)  # would be better to return to list instead once available
    else:  # ask user to confirm deleting car
        return render(request, 'cars/delete_car.html', {'car_detail': car})  # maybe shouldn't be indented


@login_required()
def refuel_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id, user_id=request.user)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RefuelForm(request.POST, mileage_validation=car.total_mileage)
        # check whether it's valid:
        if form.is_valid():
            print form.cleaned_data['date']
            print form.cleaned_data['mileage']
            print form.cleaned_data['litres']
            print form.cleaned_data['price']
            print form.cleaned_data['full_tank']
            messages.success(request, "Your car was refueled!")
            return redirect(list_cars)  # would be better to return to list instead once available
        else:  # form not valid
            messages.error(request, "Please correct the highlighted fields")
    else:   # if a GET (or any other method) we'll create a blank form
        form = RefuelForm(mileage_validation=car.total_mileage)

    return render(request, 'cars/refuel_car.html', {'form': form, 'car_detail': car})
