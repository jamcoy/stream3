from django.shortcuts import render, redirect, get_object_or_404
from urllib2 import urlopen
from .forms import PlateForm, RefuelForm
import json
from django.contrib.auth.decorators import login_required
from .models import Car, Refuel
from django.contrib import messages
from decimal import *


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
    refuel_count = Refuel.objects.filter(car_id=car_id).count()
    car_statistic = {}

    # new car
    if refuel_count == 0:
        car_statistic['economy'] = "TBD"
        car_statistic['miles'] = "TBD"
        car_statistic['fuel'] = "TBD"
        car_statistic['ppm'] = "TBD"
        car_statistic['expenditure'] = "TBD"
        car_statistic['fuel_cost'] = "TBD"
        messages.success(request, "Data will start to become available after your first \
                                   refuel.  For best results, fill your tank.")

    # first refuel
    elif refuel_count == 1:
        first_refuel = Refuel.objects.filter(car_id=car_id)[:1].get()
        car_statistic['economy'] = "TBD"
        car_statistic['miles'] = "TBD"
        car_statistic['fuel'] = "TBD"
        car_statistic['ppm'] = "TBD"
        car_statistic['expenditure'] = first_refuel.price
        car_statistic['fuel_cost'] = "TBD"
        messages.success(request, "The remaining fields will show information after your second refuel.  For best \
                                   results, fill your tank.")
    # subsequent refuels
    else:
        latest_refuel = Refuel.objects.filter(car_id=car_id).latest('date_time_added')

        # full tank, no missed refuels
        if latest_refuel.full_tank and not latest_refuel.missed_refuels:
            total_fuel = 0
            total_mileage = 0
            total_cost = 0
            all_refuels = Refuel.objects.filter(car_id=car_id, valid_for_calculations=True)
            for refuel in all_refuels:
                total_fuel += refuel.litres
                total_mileage += refuel.mileage
                total_cost += refuel.price
            car_statistic['economy'] = round(total_mileage / (total_fuel / Decimal(4.545454)), 1)
            car_statistic['miles'] = Decimal(total_mileage).quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)
            car_statistic['fuel'] = Decimal(total_fuel).quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)
            car_statistic['expenditure'] = Decimal(total_cost).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
            car_statistic['ppm'] = round((total_cost / total_mileage) * 100, 1)
            car_statistic['fuel_cost'] = round(((total_cost * 100) / total_fuel), 1)

        # Not a full tank
        elif not latest_refuel.full_tank and not latest_refuel.missed_refuels:
            messages.warning(request, "Your last refuel was not a full tank. Data will not be updated until your next \
                                       full-tank refuel, but will continue to contribute to your overall figures.")

        # missed logging a refuel
        elif latest_refuel.full_tank and latest_refuel.missed_refuels:
            messages.warning(request, "Due to missing one or more refuels, tracking is paused until your next refuel.")

        # not a full tank AND missed logging a refuel
        else:
            messages.warning(request, "Due to missing one or more refuels, tracking is paused until your next refuel. \
                                       Filling your tank will give the best results.")

    cars_list = Car.objects.filter(user_id=request.user)
    return render(request, 'cars/cars.html', {'car_detail': car_detail,
                                              'cars_list': cars_list,
                                              'car_statistic': car_statistic})


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
        latest_car = Car.objects.filter(user_id=request.user).latest('date_added')  # django is asynchronous, so save() has completed
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
        form = RefuelForm(request.POST, mileage_validation=car.odometer)
        # check whether it's valid:
        if form.is_valid():
            valid_for_calcs = False
            if Refuel.objects.filter(car_id=car_id).count() == 0:
                mileage = 0
            else:
                mileage = form.cleaned_data['mileage'] - car.odometer
                valid_for_calcs = True

            # record refuel data with calculated mileage
            r = Refuel(user=request.user,
                       car=car,
                       mileage=mileage,
                       date_time_added=form.cleaned_data['date'],
                       litres=form.cleaned_data['litres'],
                       price=form.cleaned_data['price'],
                       full_tank=form.cleaned_data['full_tank'],
                       missed_refuels=form.cleaned_data['missed_refuels'],
                       valid_for_calculations=valid_for_calcs)
            r.save()

            # update car's odometer reading
            car.odometer = form.cleaned_data['mileage']
            car.save()

            message = "Your car was refueled."
            if form.cleaned_data['full_tank'] == "False":  # String because can't get django radio to play with bools
                message += " Fill the tank for better results."
            if form.cleaned_data['missed_refuels'] == "True":  # String cos can't get django radio to play with bools
                message += " Tracking paused until next refuel due to missed refuel."
            messages.success(request, message)
            return redirect(list_cars)  # would be better to return to list instead once available

        else:  # form not valid
            messages.error(request, "Please correct the highlighted fields")
    else:   # if a GET (or any other method) we'll create a blank form
        form = RefuelForm(mileage_validation=car.odometer)

    return render(request, 'cars/refuel_car.html', {'form': form, 'car_detail': car})
