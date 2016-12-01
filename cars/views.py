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

    car_statistic = {}
    # latest_refuel = Refuel.objects.filter(car_id=car_id).latest('date_time_added')

    total_litres = 0
    total_mileage = 0
    total_price = 0

    refuel_count = Refuel.objects.filter(car_id=car_id).count()
    if refuel_count > 1:
        all_refuels = Refuel.objects.filter(car_id=car_id).order_by('-date_time_added')

        # Economy algorithm, accounting for user missing refuels, or partial tank refuels
        part_tanks_litres = 0
        part_tanks_price = 0
        part_tanks_mileage = 0
        i = 0
        full_tank_found = False

        for refuel in all_refuels:
            print refuel
            previous_refuel = i + 1
            if previous_refuel == refuel_count:
                break  # reached end

            # collect up consecutive partial tanks, unless user missed logging refuel and only if we've seen a full tank
            if full_tank_found and not refuel.full_tank and not refuel.missed_refuels:
                part_tanks_litres += refuel.litres
                part_tanks_price += refuel.price
                part_tanks_mileage += (refuel.odometer - all_refuels[previous_refuel].odometer)

            # add full tanks and collected part tanks to total, unless user has missed logging a refuel
            elif refuel.full_tank and not refuel.missed_refuels:
                full_tank_found = True
                total_litres += part_tanks_litres
                total_litres += refuel.litres
                total_price += part_tanks_price
                total_price += refuel.price
                total_mileage += part_tanks_mileage
                total_mileage += (refuel.odometer - all_refuels[previous_refuel].odometer)
                part_tanks_litres = 0
                part_tanks_price = 0
                part_tanks_mileage = 0

            # user has missed logging a refuel - full and collected part tanks to this point must be disregarded
            else:
                part_tanks_litres = 0
                part_tanks_price = 0
                part_tanks_mileage = 0
            i += 1

        # prepare the figures
        car_statistic['economy'] = round(total_mileage / (total_litres / Decimal(4.545454)), 1)
        car_statistic['miles'] = "{:,}".format(Decimal(total_mileage).quantize(Decimal('1'),
                                                                               rounding=ROUND_HALF_EVEN))
        car_statistic['fuel'] = "{:,}".format(Decimal(total_litres).quantize(Decimal('1'), rounding=ROUND_HALF_EVEN))
        car_statistic['ppm'] = round((total_price / total_mileage) * 100, 1)
        car_statistic['fuel_cost'] = round(((total_price * 100) / total_litres), 1)
        if total_price < 1000:
            car_statistic['expenditure'] = Decimal(total_price).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
        else:
            car_statistic['expenditure'] = "{:,}".format(Decimal(total_price).quantize(Decimal('1'),
                                                                                      rounding=ROUND_HALF_EVEN))

    # new cars
    else:
        car_statistic['economy'] = "TBD"
        car_statistic['miles'] = "TBD"
        car_statistic['fuel'] = "TBD"
        car_statistic['ppm'] = "TBD"
        car_statistic['fuel_cost'] = "TBD"
        car_statistic['expenditure'] = "TBD"

        # new car that had an initial reading on it's 1st refuel
        if refuel_count == 1 and car_detail.odometer_initial is not None:
            messages.success(request, "Data will be available after your first valid full-tank refuel.")

        elif refuel_count == 1:
            messages.success(request, "A valid full tank refuel is required to show some results. Partial refuels \
                                       will contribute to later results, so long as not followed by a missed refuel.")
        else:
            messages.success(request, "Data will be available after two full-tank refuels.")

        ''' # not a full tank, but didn't miss a refuel - update message
        if not latest_refuel.full_tank and not latest_refuel.missed_refuels:
            messages.warning(request, "Your last refuel was not a full tank. Data will not be updated until your next \
                                       full-tank refuel, but will continue to contribute to your overall figures, \
                                       so long as you don't miss logging any refuels.")

        # missed logging a refuel
        elif latest_refuel.missed_refuels:
            messages.warning(request, "Due to missing one or more refuels, tracking is paused until your next full \
                                       tank refuel.")'''

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
                    odometer_initial=form.cleaned_data['odo_reading'])
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

    new_car_with_odometer = False

    # set things up for our odometer validation
    odometer_validation = 0
    refuel_count = Refuel.objects.filter(car_id=car_id).count()
    if refuel_count > 0:
        odometer_validation = Refuel.objects.filter(car_id=car_id).latest('date_time_added').odometer
    elif car.odometer_initial is not None:
        odometer_validation = car.odometer_initial
        new_car_with_odometer = True

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RefuelForm(request.POST, odometer_validation=odometer_validation,
                          skip_missed_refuel_question=new_car_with_odometer)

        # check if form is valid
        if form.is_valid():

            # refueling a new car for the first time that was added to the system without an odometer reading
            if not new_car_with_odometer and refuel_count == 0:
                form.cleaned_data['missed_refuels'] = True  # obviously no record of any previous refuels

            # record refuel data with calculated mileage
            r = Refuel(user=request.user,
                       car=car,
                       odometer=form.cleaned_data['odometer'],
                       date_time_added=form.cleaned_data['date'],
                       litres=form.cleaned_data['litres'],
                       price=form.cleaned_data['price'],
                       full_tank=form.cleaned_data['full_tank'],
                       missed_refuels=form.cleaned_data['missed_refuels'])
            r.save()

            return redirect(cars, car.pk)

        else:  # form not valid
            messages.error(request, "Please correct the highlighted fields")
    else:   # if a GET (or any other method) we'll create a blank form
        form = RefuelForm(odometer_validation=odometer_validation, skip_missed_refuel_question=new_car_with_odometer)

    return render(request, 'cars/refuel_car.html', {'form': form, 'car_detail': car})
