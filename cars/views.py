# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from urllib2 import urlopen
from .forms import PlateForm, RefuelForm, ImageForm
import json
from django.contrib.auth.decorators import login_required
from .models import Car, Refuel
from django.contrib import messages
from decimal import *
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone
import re


def list_of_cars(user):
    return Car.objects.filter(user_id=user)\
                      .annotate(car=Concat('make', V(' '), 'model', V(' '), 'sub_model'))\
                      .order_by('car')


@login_required()
def list_cars(request):
    if Car.objects.filter(user_id=request.user):
        first_car = Car.objects.filter(user_id=request.user)[:1].get()
        return redirect(car_stats, first_car.pk)  # redirects to user's 1st car
    else:  # if user has no cars, send them to the add car form
        form = PlateForm()
        return render(request, 'cars/add_car.html', {'form': form})


@login_required()
def refuel_history(request, car_id):
    car_detail = get_object_or_404(Car, pk=car_id, user_id=request.user)
    refuel_count = Refuel.objects.filter(car_id=car_id).count()
    refuels = {}

    if refuel_count > 0:
        refuels = Refuel.objects.filter(car_id=car_id).order_by('-date')
        i = 0
        for refuel in refuels:
            refuel.odometer = format(Decimal(refuel.odometer).quantize(Decimal('1'), rounding=ROUND_HALF_EVEN))
            if refuel.litres > 0:
                refuel.litre_price = round((refuel.price * 100 / refuel.litres), 1)

            # full tanks need to be flagged if they are included in results so this can be show to user
            if refuel.full_tank:
                for l in range(i, refuel_count - 1):
                    if l == refuel_count:  # shouldn't be able to get here if database good, but best to be safe!
                        refuel.full_tank_include = False
                        break
                    # if a full tank was preceded by a part tank with missed preceding missed refuels, exclude
                    elif not refuels[l + 1].full_tank and refuels[l + 1].missed_refuels:
                        refuel.full_tank_include = False
                        break
                    elif refuels[l + 1].full_tank:
                        refuel.full_tank_include = True
                        break

            # part tanks need to know the status of what precedes and follows to show the user if they're included
            elif not refuel.full_tank:
                for j in range(i, -1, -1):
                    if refuel.missed_refuels:
                        refuel.part_tank_status = "exclude"
                        break
                    elif j == 0:
                        refuel.part_tank_status = "unknown"  # most recent tank - don't yet know what will follow
                        break
                    elif refuels[j - 1].missed_refuels:
                        refuel.part_tank_status = "exclude"
                        break

                    elif refuels[j - 1].full_tank:  # Also need to check what preceded.
                        for k in range(i, refuel_count - 1):
                            if k == refuel_count:  # shouldn't be able to get here if database good, but best be safe!
                                refuel.part_tank_status = "exclude"
                                break
                            elif refuels[k + 1].missed_refuels and not refuels[k + 1].full_tank:
                                refuel.part_tank_status = "exclude"
                                break
                            elif refuels[k + 1].full_tank:
                                refuel.part_tank_status = "include"
                                break
                        break
            i += 1

    cars_list = list_of_cars(request.user)
    return render(request, 'cars/refuel_history.html', {'car_detail': car_detail,
                                                        'cars_list': cars_list,
                                                        'refuels': refuels})


@login_required()
def car_details(request, car_id):
    car_detail = get_object_or_404(Car, pk=car_id, user_id=request.user)
    refuel_count = Refuel.objects.filter(car_id=car_id).count()
    latest_refuel = {}
    if refuel_count > 0:
        latest_refuel = Refuel.objects.filter(car_id=car_id).latest('date')
        latest_refuel.odometer = "{:,}".format(int(latest_refuel.odometer))
    cars_list = list_of_cars(request.user)
    return render(request, 'cars/car_details.html', {'car_detail': car_detail,
                                                     'cars_list': cars_list,
                                                     'refuel': latest_refuel})


def car_stats_totals(car_id):
    all_refuels = Refuel.objects.filter(car_id=car_id).order_by('date')

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
                part_price += refuel.price

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

    return {'litres': total_litres,
            'miles': total_mileage,
            'price': total_price,
            'previous_refuel': previous_refuel}


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

        messages.info(request, "Tracking starts after your first full tank refuel.  Data will be available \
                                   following your second full tank refuel.  Always try to fill your tank.")

    # all other cars
    else:
        refuel_totals = car_stats_totals(car_id)
        total_litres = refuel_totals['litres']
        total_mileage = refuel_totals['miles']
        total_price = refuel_totals['price']
        previous_refuel = refuel_totals['previous_refuel']

        latest_refuel = Refuel.objects.filter(car_id=car_id).latest('date')

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

    cars_list = list_of_cars(request.user)
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
            plate = re.sub('[\W_]+', '', form.cleaned_data['your_reg'])
            page = urlopen(url + plate)
            car_details = json.loads(page.read())
            car_details['yourReg'] = form.cleaned_data['your_reg']
            request.session['full_car_details'] = car_details
            if 'error' in car_details:
                if car_details['error'] == 1 and car_details['message'] == "Demo account can only be used for VRMs" \
                                                                           " beginning with MT09 or FH51":
                    error_message = "EasyFuelTracker is currently operating on a demo API account that can only" \
                                    " be used for plates beginning with MT09 or FH51"
                    return render(request, "cars/add_car_error.html", {'plate': form.cleaned_data['your_reg'],
                                                                       'error': error_message})
                elif car_details['error'] == 1:
                    return render(request, "cars/add_car_error.html", {'plate': form.cleaned_data['your_reg'],
                                                                       'error': "Invalid plate"})
                elif car_details['error'] == 0:
                    return render(request, "cars/add_car_error.html", {'plate': form.cleaned_data['your_reg'],
                                                                       'error': "Plate not found"})
                else:
                    return render(request, "cars/add_car_error.html", {'plate': form.cleaned_data['your_reg'],
                                                                       'error': "Unknown error"})
            else:
                if car_details['yearOfManufacture'] == "" or car_details['cylinderCapacity'] == "" \
                        or car_details['transmission'] == "" or car_details['fuelType'] == "" \
                        or car_details['model'] == "" or car_details['make'] == "":
                    car_details['exclude_from_collation'] = True
                    car_details['exclude_from_collation_reason'] = "incomplete details"
                else:
                    car_details['exclude_from_collation'] = False
                    car_details['exclude_from_collation_reason'] = ""
                return render(request, "cars/add_car_details.html", {'car_details': car_details})

    else:  # if a GET (or any other method) we'll create a blank form
        form = PlateForm()
        return render(request, 'cars/add_car.html', {'form': form})


@login_required()
def add_car_details(request):
    # validation not required here - user cannot edit anything - just confirming right vehicle
    if request.method == 'POST':
        new_car_details = request.session['full_car_details']  # pass to confirmation page using session variable
        request.session['full_car_details'] = ""

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
                exclude_from_collation=new_car_details['exclude_from_collation'],
                exclude_from_collation_reason=new_car_details['exclude_from_collation_reason'],
                doors=new_car_details['numberOfDoors'])
        c.save()

        latest_car = Car.objects.filter(user_id=request.user).latest('date_added')  # django is asynchronous
        return redirect(car_stats, latest_car.pk)

    else:
        form = PlateForm()
        return render(request, 'cars/add_car.html', {'form': form})


@login_required()
def refuel_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id, user_id=request.user)

    # set things up for our odometer validation
    odometer_validation = 0
    date_validation = 0
    new_car = False
    refuel_count = Refuel.objects.filter(car_id=car_id).count()
    if refuel_count > 0:
        odometer_validation = Refuel.objects.filter(car_id=car_id).latest('date').odometer
        date_validation = Refuel.objects.filter(car_id=car_id).latest('date').date
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
                       date=form.cleaned_data['date'],
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

    cars_list = list_of_cars(request.user)
    return render(request, 'cars/refuel_car.html', {'form': form,
                                                    'car_detail': car,
                                                    'cars_list': cars_list,
                                                    'new_car': new_car})


@login_required()
def upload_image(request, car_id):
    car = get_object_or_404(Car, pk=car_id, user_id=request.user)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageForm(request.POST, request.FILES, instance=car)
        # check whether it's valid:
        if form.is_valid():
            car = form.save(commit=False)
            car.save()
            return redirect(car_stats, car.pk)
    else:  # if a GET (or any other method) we'll create a blank form
        form = ImageForm(instance=car)
        cars_list = list_of_cars(request.user)
        return render(request, 'cars/upload_image.html', {'form': form,
                                                          'cars_list': cars_list,
                                                          'car_detail': car})


@login_required()
def delete_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id, user_id=request.user)
    if request.method == 'POST':  # user has confirmed deleting car
        car.delete()
        messages.success(request, "Your car was deleted!")
        return redirect(list_cars)
    else:  # ask user to confirm deleting car
        cars_list = list_of_cars(request.user)
        return render(request, 'cars/delete_car.html', {'cars_list': cars_list,
                                                        'car_detail': car})


@login_required()
def select_chart(request):
    chart_type = request.GET.get('chart_type', None)
    chart_range = request.GET.get('chart_range', None)
    car_id = request.GET.get('car_id', None)
    today = timezone.now()
    start_date = today-timedelta(days=int(chart_range))
    refuels = Refuel.objects.filter(car_id=car_id, date__gte=start_date).order_by('date')
    total_litres = 0
    total_price = 0
    total_mileage = 0
    part_litres = 0
    part_price = 0
    start_mileage = 0
    found_start_point = False

    for refuel in refuels:
        refuel.formatted_date = refuel.date.strftime('%Y-%m-%dT%H:%M:%S')
        refuel.valid_end_point = False
        refuel.contains_part_refuels = False

    i = 0
    for refuel in refuels:
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
                part_price += refuel.price

        # valid end point (and next start point)
        else:
            total_litres += part_litres + refuel.litres
            total_price += part_price + refuel.price
            total_mileage += refuel.odometer - start_mileage

            refuel.end_point_litres = total_litres
            refuel.end_point_price = total_price
            refuel.end_point_mileage = total_mileage
            refuel.valid_end_point = True  # we only want to chart valid end points

            if part_litres > 0:
                refuel.contains_part_refuels = True  # flag to user that a reading includes part refuels

            # only reset these after reaching the valid end-point
            total_litres = 0
            total_price = 0
            total_mileage = 0
            part_litres = 0
            part_price = 0
            start_mileage = refuel.odometer

        i += 1

    data_model = []
    if chart_type == "expenditure":
        data_model = [{
                'date_time': refuel.formatted_date,
                'data_value': str(refuel.end_point_price),
                'includes_partial_refuels': str(refuel.contains_part_refuels)
            } for refuel in refuels if refuel.valid_end_point]
        data_model.append({'label': "Refuel cost"})
        data_model.append({'units': "£"})
        data_model.append({'units_position': "before"})
    elif chart_type == "fuel":
        data_model = [{
                'date_time': refuel.formatted_date,
                'data_value': str(refuel.end_point_litres),
                'includes_partial_refuels': str(refuel.contains_part_refuels)
            } for refuel in refuels if refuel.valid_end_point]
        data_model.append({'label': "Litres of fuel"})
        data_model.append({'units': "l"})
        data_model.append({'units_position': "after"})
    elif chart_type == "price":
        data_model = [{
                'date_time': refuel.formatted_date,
                'data_value': str(round(((refuel.end_point_price * 100) / refuel.end_point_litres), 1)),
                'includes_partial_refuels': str(refuel.contains_part_refuels)
            } for refuel in refuels if refuel.valid_end_point]
        data_model.append({'label': "Pump price"})
        data_model.append({'units': "p / l"})
        data_model.append({'units_position': "after"})
    elif chart_type == "economy":
        data_model = [{
                'date_time': refuel.formatted_date,
                'data_value': str(round(refuel.end_point_mileage / (refuel.end_point_litres / Decimal(4.545454)), 1)),
                'includes_partial_refuels': str(refuel.contains_part_refuels)
            } for refuel in refuels if refuel.valid_end_point]
        data_model.append({'label': "Fuel economy"})
        data_model.append({'units': "MPG"})
        data_model.append({'units_position': "after"})
    elif chart_type == "mileage":
        data_model = [{
                'date_time': refuel.formatted_date,
                'data_value': str(refuel.end_point_mileage),
                'includes_partial_refuels': str(refuel.contains_part_refuels)
            } for refuel in refuels if refuel.valid_end_point]
        data_model.append({'label': "Mileage"})
        data_model.append({'units': "miles"})
        data_model.append({'units_position': "after"})
    return HttpResponse(json.dumps(data_model), content_type='application/json')

