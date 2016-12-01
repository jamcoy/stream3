# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError


class PlateForm(forms.Form):
    your_reg = forms.CharField(label='',
                               max_length=20,
                               widget=forms.TextInput(attrs={'class': 'uk-rear-plate'}))


class OdometerForm(forms.Form):
    odo_reading = forms.DecimalField(label='Current odometer reading \
                                            (supplying a reading now will give quicker results but is not required)',
                                     min_value=0,
                                     max_value=10000000,
                                     required=False)


class RefuelForm(forms.Form):
    date = forms.CharField(label='Date and Time',
                           initial='Now')
    odometer = forms.DecimalField(label='Total mileage')
    litres = forms.DecimalField(label='Litres of fuel', min_value=0.1, max_value=500)
    price = forms.DecimalField(label='Price paid (£)', min_value=0.01, max_value=750)
    full_tank = forms.ChoiceField(label="Did you fill the tank?",
                                  choices=[(True, 'Yes. I filled the tank.'),
                                           (False, 'No. I partially filled the tank.')],
                                  widget=forms.RadioSelect(),
                                  required=True)

    def __init__(self, *args, **kwargs):
        self.odometer_validation = kwargs.pop('odometer_validation')
        skip_question = kwargs.pop('skip_missed_refuel_question')
        super(RefuelForm, self).__init__(*args, **kwargs)
        # only show the question about missing a refuel if it's not a new car, or not a new car with an odometer reading
        if skip_question:
            self.fields['missed_refuels'] = forms.ChoiceField(label="Did you miss logging a previous refuel?",
                                                              choices=[(True, 'Yes. I forgot to log a refuel.'),
                                                                       (False, 'No refuels missed.')],
                                                              widget=forms.RadioSelect(),
                                                              required=True)

    def clean_odometer(self):
        odometer = self.cleaned_data['odometer']
        if odometer < self.odometer_validation:
            raise ValidationError(
                "That mileage is no higher than your last reading (" + str(self.odometer_validation) + ")"
            )
        return odometer
