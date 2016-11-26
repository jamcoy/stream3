from django.shortcuts import render
from urllib2 import urlopen
from .forms import PlateForm
import json
from django.contrib.auth.decorators import login_required


@login_required()
def cars(request):
    return render(request, 'cars/cars.html')


@login_required()
def add_car(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlateForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            url = "https://dvlasearch.appspot.com/DvlaSearch?apikey=DvlaSearchDemoAccount&licencePlate="
            print form.cleaned_data['your_reg']
            page = urlopen(url + form.cleaned_data['your_reg'])
            car_details = json.loads(page.read())
            car_details['yourReg'] = form.cleaned_data['your_reg']
            check = True  # expand upon this!
            if check:
                return render(request, "cars/add_car.html", {'car_details': car_details})
            else:
                # generate an error
                pass

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlateForm()

    return render(request, 'cars/add_car.html', {'form': form})
