# -*- coding: utf-8 -*-
from django import forms


class PlateForm(forms.Form):
    your_reg = forms.CharField(label='',
                               max_length=20,
                               widget=forms.TextInput(attrs={'class': 'uk-rear-plate'}))


class RefuelForm(forms.Form):
    FULL_TANK_CHOICES = [(True, 'Full tank'),
                         (False, 'Partial refill')]
    date = forms.CharField(label='Date')
    mileage = forms.CharField(label='Total mileage')
    litres = forms.CharField(label='Litres of fuel')
    price = forms.CharField(label='Price paid (£)')
    full_tank = forms.ChoiceField(choices=FULL_TANK_CHOICES, widget=forms.RadioSelect())
