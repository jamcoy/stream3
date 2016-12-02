from django.shortcuts import render, redirect, get_object_or_404
from urllib2 import urlopen
from .forms import PlateForm, RefuelForm
import json
from django.contrib.auth.decorators import login_required
from .models import Car, Refuel
from django.contrib import messages
from decimal import *
from django.db.models import Value as V
from django.db.models.functions import Concat


def list_of_cars(request):  # not a view
    return Car.objects.filter(user_id=request.user)\
                      .annotate(car=Concat('make', V(' '), 'model', V(' '), 'sub_model'))\
                      .order_by('car')


@login_required()
def list_cars(request):
    if Car.objects.filter(user_id=request.user):
        first_car = Car.objects.filter(user_id=request.user)[:1].get()
        return redirect(car_stats, first_car.pk)  # for the moment it redirects to user's 1st car
    else:  # if user has no cars, send them to the add car form
        form = PlateForm()
        return render(request, 'cars/add_car.html', {'form': form})  # maybe shouldn't be indented


@login_required()
def refuel_history(request, car_id):
    car_detail = get_object_or_404(Car, pk=car_id, user_id=request.user)
    refuel_count = Refuel.objects.filter(car_id=car_id).count()
    refuels = {}  # is this necessary???
    if refuel_count > 0:
        refuels = Refuel.objects.filter(car_id=car_id).order_by('-date_time_added')
        for refuel in refuels:
            if refuel.litres > 0:
                refuel.litre_price = round((refuel.price * 100 / refuel.litres), 1)
    cars_list = list_of_cars(request)
    return render(request, 'cars/refuel_history.html', {'car_detail': car_detail,
                                                        'cars_list': cars_list,
                                                        'refuels': refuels})


@login_required()
def car_details(request, car_id):
    car_detail = get_object_or_404(Car, pk=car_id, user_id=request.user)
    cars_list = list_of_cars(request)
    refuel_count = Refuel.objects.filter(car_id=car_id).count()
    latest_refuel = {}  # is this necessary???
    if refuel_count > 0:
        latest_refuel = Refuel.objects.filter(car_id=car_id).latest('date_time_added')
        latest_refuel.odometer = "{:,}".format(int(latest_refuel.odometer))
    return render(request, 'cars/car_details.html', {'car_detail': car_detail,
                                                     'cars_list': cars_list,
                                                     'refuel': latest_refuel})


@login_required()
def car_stats(request, car_id):
    car_detail = get_object_or_404(Car, pk=car_id, user_id=request.user)
    car_statistic = {}

    refuel_count = Refuel.objects.filter(car_id=car_id).count()

    # new cars
    if refuel_count < 2:
        car_statistic['economy'] = "TBD"
        car_statistic['miles'] = "TBD"
        car_statistic['fuel'] = "TBD"
        car_statistic['ppm'] = "TBD"
        car_statistic['fuel_cost'] = "TBD"
        car_statistic['expenditure'] = "TBD"

        messages.success(request, "Tracking starts after your first full tank refuel.  Data will be available \
                                   following your second full tank refuel.")

    # all other cars
    else:
        all_refuels = Refuel.objects.filter(car_id=car_id).order_by('date_time_added')
        latest_refuel = Refuel.objects.filter(car_id=car_id).latest('date_time_added')

        # Economy algorithm, accounting for user missing refuels, or partial tank refuels
        total_litres = 0
        total_mileage = 0
        total_price = 0
        part_litres = 0
        part_price = 0
        start_mileage = 0
        found_start_point = False
        previous_refuel = []  # used in subsequent message to user
        i = 0

        for refuel in all_refuels:

            # user missed a refuel - reset everything - but it can still be a valid start point if it was a full tank
            if refuel.missed_refuels:
                part_litres = 0
                part_price = 0
                # valid start point
                if refuel.full_tank:
                    start_mileage = refuel.odometer
                    found_start_point = True
                # not valid start point
                else:
                    found_start_point = False

            # valid start point
            elif refuel.full_tank and found_start_point is False:
                start_mileage = refuel.odometer
                found_start_point = True

            # part filled tanks
            elif refuel.full_tank is False:
                # only include a part tank that follows a valid start point
                if found_start_point:
                    part_litres += refuel.litres
                    part_price += refuel.litres

            # valid end point (and next start point)
            else:
                total_litres += part_litres + refuel.litres
                total_price += part_price + refuel.price
                total_mileage += refuel.odometer - start_mileage
                part_litres = 0
                part_price = 0
                start_mileage = refuel.odometer
                previous_refuel = all_refuels[i - 1]

            i += 1

        # prepare the figures
        if total_litres > 0 and total_mileage > 0 and total_price > 0:
            car_statistic['economy'] = round(total_mileage / (total_litres / Decimal(4.545454)), 1)
            car_statistic['miles'] = "{:,}".format(Decimal(total_mileage).quantize(Decimal('1'),
                                                                                   rounding=ROUND_HALF_EVEN))
            car_statistic['fuel'] = "{:,}".format(Decimal(total_litres).quantize(Decimal('1'),
                                                                                 rounding=ROUND_HALF_EVEN))
            car_statistic['ppm'] = round((total_price / total_mileage) * 100, 1)
            car_statistic['fuel_cost'] = round(((total_price * 100) / total_litres), 1)
            if total_price < 1000:
                car_statistic['expenditure'] = Decimal(total_price).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
            else:
                car_statistic['expenditure'] = "{:,}".format(Decimal(total_price).quantize(Decimal('1'),
                                                                                           rounding=ROUND_HALF_EVEN))

            # tracking resumed
            if latest_refuel.full_tank and not latest_refuel.missed_refuels and previous_refuel.missed_refuels \
                    and refuel_count > 2:
                messages.warning(request, "Tracking resumed after missing previous refuel(s).")

            # not a full tank, but didn't miss a refuel - update message
            if not latest_refuel.full_tank and not latest_refuel.missed_refuels:
                messages.warning(request, "Your last refuel was not a full tank. Displayed data will not be updated \
                                           until your next full-tank refuel.  Partial refuels will contribute to your \
                                           overall data, so long as you haven't missed logging any refuels.")

            # missed logging a refuel
            elif latest_refuel.missed_refuels:
                messages.warning(request, "Due to missing one or more refuels, tracking is paused until your next full \
                                           tank refuel.")

        # new cars with multiple bad refuels
        else:
            car_statistic['economy'] = "TBD"
            car_statistic['miles'] = "TBD"
            car_statistic['fuel'] = "TBD"
            car_statistic['ppm'] = "TBD"
            car_statistic['fuel_cost'] = "TBD"
            car_statistic['expenditure'] = "TBD"

            messages.success(request, "You MUST complete at least TWO FULL TANK refuels to get some results!")

    cars_list = list_of_cars(request)
    return render(request, 'cars/car_stats.html', {'car_detail': car_detail,
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
    # validation not required here - user cannot edit anything - just confirming right vehicle
    if request.method == 'POST':
        new_car_details = request.session['full_car_details']  # pass to confirmation page using session variable
        request.session['full_car_details'] = ""  # necessary to clear??

        # check if the new car has a sub_model
        model_components_count = len(new_car_details['model'].split(' '))
        model = new_car_details['model'].split(' ', 1)[0]
        if model_components_count > 1:
            sub_model = new_car_details['model'].split(' ', 1)[1]
        else:
            sub_model = ""

        # save new car in database
        c = Car(user=request.user,
                make=new_car_details['make'],
                model=model,
                sub_model=sub_model,
                colour=new_car_details['colour'],
                year_of_manufacture=new_car_details['yearOfManufacture'],
                cylinder_capacity=new_car_details['cylinderCapacity'],
                transmission=new_car_details['transmission'],
                fuel_type=new_car_details['fuelType'],
                co2=new_car_details['co2Emissions'],
                doors=new_car_details['numberOfDoors'])
        c.save()

        latest_car = Car.objects.filter(user_id=request.user).latest('date_added')  # django is asynchronous
        return redirect(car_stats, latest_car.pk)

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

    # set things up for our odometer validation
    odometer_validation = 0
    date_validation = 0
    new_car = False
    refuel_count = Refuel.objects.filter(car_id=car_id).count()
    if refuel_count > 0:
        odometer_validation = Refuel.objects.filter(car_id=car_id).latest('date_time_added').odometer
        date_validation = Refuel.objects.filter(car_id=car_id).latest('date_time_added').date_time_added
    else:
        new_car = True

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RefuelForm(request.POST, odometer_validation=odometer_validation,
                          date_validation=date_validation,
                          skip_missed_refuel_question=new_car)

        # check if form is valid
        if form.is_valid():

            # refueling a new car for the first time
            if refuel_count == 0:
                form.cleaned_data['missed_refuels'] = True  # obviously no record of any previous refuels
                form.cleaned_data['litres'] = 0
                form.cleaned_data['price'] = 0

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

            return redirect(car_stats, car.pk)

        else:  # form not valid
            messages.error(request, "Please correct the highlighted fields")
    else:   # if a GET (or any other method) we'll create a blank form
        form = RefuelForm(odometer_validation=odometer_validation,
                          date_validation=date_validation,
                          skip_missed_refuel_question=new_car)

    return render(request, 'cars/refuel_car.html', {'form': form, 'car_detail': car, 'new_car': new_car})
