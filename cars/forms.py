# -*- coding: utf-8 -*-
from django import forms


class PlateForm(forms.Form):
    your_reg = forms.CharField(label='',
                               max_length=20,
                               widget=forms.TextInput(attrs={'class': 'uk-rear-plate'}))


class RefuelForm(forms.Form):
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
