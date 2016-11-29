# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError


class PlateForm(forms.Form):
    your_reg = forms.CharField(label='',
                               max_length=20,
                               widget=forms.TextInput(attrs={'class': 'uk-rear-plate'}))


class RefuelForm(forms.Form):
    FULL_TANK_CHOICES = [(True, 'Yes, I filled the tank'),
                         (False, 'No, I partially filled the tank')]
    MISSED_PREVIOUS_REFILL = [(False, 'No refuels missed'),
                              (True, 'Yes, I forgot to log a refuel')]
    date = forms.CharField(label='Date and Time',
                           initial='Now')
    mileage = forms.DecimalField(label='Total mileage')
    litres = forms.DecimalField(label='Litres of fuel', min_value=0.1, max_value=500)
    price = forms.DecimalField(label='Price paid (£)', min_value=0.01, max_value=750)
    full_tank = forms.ChoiceField(label="Did you fill the tank?",
                                  choices=FULL_TANK_CHOICES,
                                  widget=forms.RadioSelect(),
                                  required=True)
    missed_refuels = forms.ChoiceField(label="Did you miss any previous refuels?",
                                       choices=MISSED_PREVIOUS_REFILL,
                                       widget=forms.RadioSelect(),
                                       required=True)

    def __init__(self, *args, **kwargs):
        self.mileage_validation = kwargs.pop('mileage_validation')
        super(RefuelForm, self).__init__(*args, **kwargs)

    def clean_mileage(self):
        mileage = self.cleaned_data['mileage']
        if mileage < self.mileage_validation:
            raise ValidationError(
                "That mileage is no higher than your last refuel (" + str(self.mileage_validation) + ")"
            )
        return mileage


class RefuelFormViaCar(forms.Form):
    FULL_TANK_CHOICES = [(True, 'Full tank'),
                         (False, 'Partial refill')]
    date = forms.CharField(label='Date',
                           initial='Today')
    mileage = forms.DecimalField(label='Total mileage')
    litres = forms.DecimalField(label='Litres of fuel', min_value=0.1, max_value=500)
    price = forms.DecimalField(label='Price paid (£)', min_value=0.01, max_value=750)
    full_tank = forms.ChoiceField(choices=FULL_TANK_CHOICES,
                                  widget=forms.RadioSelect(),
                                  required=True)

    def __init__(self, *args, **kwargs):
        self.mileage_validation = kwargs.pop('mileage_validation')
        super(RefuelForm, self).__init__(*args, **kwargs)

    def clean_mileage(self):
        mileage = self.cleaned_data['mileage']
        if mileage < self.mileage_validation:
            raise ValidationError(
                "That mileage is no higher than your last refuel (" + str(self.mileage_validation) + ")"
            )
        return mileage
