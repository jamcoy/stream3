from django.shortcuts import render, redirect, get_object_or_404
from urllib2 import urlopen
from .forms import PlateForm, RefuelForm, OdometerForm
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
    latest_refuel = []
    all_refuels = []
    total_fuel = 0
    total_mileage = 0
    total_cost = 0
    if refuel_count > 0:
        latest_refuel = Refuel.objects.filter(car_id=car_id).latest('date_time_added')
        all_refuels = Refuel.objects.filter(car_id=car_id, valid_for_calculations=True).order_by('-date_time_added')
        # If latest refuel not a full tank - filter query further
        if not latest_refuel.full_tank:
            # remove latest refuels until hitting the 1st full tank
            i = 0
            for refuel in all_refuels:
                if not refuel.full_tank:
                    i += 1
                    all_refuels = all_refuels[i:]
                    break
        for refuel in all_refuels:
            total_fuel += refuel.litres
            total_mileage += refuel.mileage
            total_cost += refuel.price

    # new cars
    if refuel_count == 0:
        car_statistic['economy'] = "TBD"
        car_statistic['miles'] = "TBD"
        car_statistic['fuel'] = "TBD"
        car_statistic['ppm'] = "TBD"
        car_statistic['fuel_cost'] = "TBD"
        car_statistic['expenditure'] = "TBD"
        if car_detail.odometer is not None:
            messages.success(request, "Data will start to become available after your first valid full-tank refuel.")
        else:
            messages.success(request, "Data will start to become available after two full-tank refuels.")

    # no valid refuel data that can be displayed (other than expenditure if first tank a full tank)
    elif len(all_refuels) == 0:
        car_statistic['economy'] = "TBD"
        car_statistic['miles'] = "TBD"
        car_statistic['fuel'] = "TBD"
        car_statistic['ppm'] = "TBD"
        car_statistic['fuel_cost'] = "TBD"
        if total_cost > 0:
            car_statistic['expenditure'] = total_cost
        else:
            car_statistic['expenditure'] = "TBD"
        messages.success(request, "Another full tank refuel is required to show some results. Partial refuels \
                                   will contribute to later results.")

    # All other refuels
    else:
        # not a full tank, but didn't miss a refuel - update message
        if not latest_refuel.full_tank and not latest_refuel.missed_refuels:
            messages.warning(request, "Your last refuel was not a full tank. Data will not be updated until your next \
                                       full-tank refuel, but will continue to contribute to your overall figures.")

        # missed logging a refuel, but was a full tank - update message
        elif latest_refuel.full_tank and latest_refuel.missed_refuels:
            messages.warning(request, "Due to missing one or more refuels, tracking is paused until your next refuel.")

        # not a full tank and missed logging a refuel - update message
        elif not latest_refuel.full_tank and latest_refuel.missed_refuels:
            messages.warning(request, "Due to missing one or more refuels, tracking is paused until your next refuel. \
                                       Filling your tank will give the best results.")

        car_statistic['economy'] = round(total_mileage / (total_fuel / Decimal(4.545454)), 1)
        car_statistic['miles'] = "{:,}".format(Decimal(total_mileage).quantize(Decimal('1'),
                                                                               rounding=ROUND_HALF_EVEN))
        car_statistic['fuel'] = "{:,}".format(Decimal(total_fuel).quantize(Decimal('1'), rounding=ROUND_HALF_EVEN))
        car_statistic['ppm'] = round((total_cost / total_mileage) * 100, 1)
        car_statistic['fuel_cost'] = round(((total_cost * 100) / total_fuel), 1)
        if total_cost < 1000:
            car_statistic['expenditure'] = Decimal(total_cost).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
        else:
            car_statistic['expenditure'] = "{:,}".format(Decimal(total_cost).quantize(Decimal('1'),
                                                                                      rounding=ROUND_HALF_EVEN))

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
                odo_form = OdometerForm(request.GET)
                return render(request, "cars/add_car_details.html", {'car_details': car_details, 'form': odo_form})
            else:
                # generate an error
                pass
    else:  # if a GET (or any other method) we'll create a blank form
        form = PlateForm()
        return render(request, 'cars/add_car.html', {'form': form})  # maybe shouldn't be indented


@login_required()
def add_car_details(request):
    if request.method == 'POST':
        form = OdometerForm(request.POST)
        if form.is_valid():
            car_details = request.session['full_car_details']  # pass to next form using session variable
            request.session['full_car_details'] = ""  # necessary to clear??
            # validation not required here - user cannot edit anything - just confirming right vehicle
            # total_mileage and previous_mileage deliberately omitted
            # the car owner will never see the model / sub_model split, but it will be used when browsing mpg data
            model = car_details['model'].split(' ', 1)[0]
            sub_model = car_details['model'].split(' ', 1)[1]  # doesn't work for cars with no sub model!
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
                    doors=car_details['numberOfDoors'],
                    odometer=form.cleaned_data['odo_reading'])
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

    # set whether or not we're working with a new car (and whether or not it has an odo reading)
    new_car = False
    new_car_no_odometer = False
    if Refuel.objects.filter(car_id=car_id).count() == 0:
        new_car = True
        if car.odometer is None:
            new_car_no_odometer = True

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RefuelForm(request.POST, mileage_validation=car.odometer,
                          skip_missed_refuel_question=new_car_no_odometer)
        # check if form is valid
        if form.is_valid():

            # refueling a new car for the first time that wasn't added to the system with an odometer reading
            if new_car_no_odometer:
                mileage = None
                refuel_valid_for_calculations = False
                missed_refuels = True  # obviously no record of any previous refuels

            elif new_car:  # with odometer reading
                mileage = form.cleaned_data['mileage'] - car.odometer
                refuel_valid_for_calculations = True
                missed_refuels = False

            # not a new car, but user has reported missing a refuel. Mark this refuel invalid for economy calculations.
            elif form.cleaned_data['missed_refuels'] == "True":
                mileage = None
                refuel_valid_for_calculations = False
                missed_refuels = True

            # Normal refuel. Calculate mileage covered and mark as valid for refuel calculations
            else:
                mileage = form.cleaned_data['mileage'] - car.odometer
                refuel_valid_for_calculations = True
                missed_refuels = False

            # record refuel data with calculated mileage
            r = Refuel(user=request.user,
                       car=car,
                       mileage=mileage,
                       date_time_added=form.cleaned_data['date'],
                       litres=form.cleaned_data['litres'],
                       price=form.cleaned_data['price'],
                       full_tank=form.cleaned_data['full_tank'],
                       missed_refuels=missed_refuels,
                       valid_for_calculations=refuel_valid_for_calculations)
            r.save()

            # update car's odometer reading
            car.odometer = form.cleaned_data['mileage']
            car.save()

            return redirect(cars, car.pk)

        else:  # form not valid
            messages.error(request, "Please correct the highlighted fields")
    else:   # if a GET (or any other method) we'll create a blank form
        form = RefuelForm(mileage_validation=car.odometer, skip_missed_refuel_question=new_car_no_odometer)

    return render(request, 'cars/refuel_car.html', {'form': form, 'car_detail': car})
