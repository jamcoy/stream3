# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Car


class PlateForm(forms.Form):
    your_reg = forms.CharField(label='',
                               max_length=20,
                               widget=forms.TextInput(attrs={'class': 'uk-rear-plate'}))


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label="Note that your image can be viewed by anyone.")

    class Meta:
        model = Car
        fields = ['image']


class RefuelForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.odometer_validation = kwargs.pop('odometer_validation')
        self.date_validation = kwargs.pop('date_validation')
        new_car = kwargs.pop('skip_missed_refuel_question')
        self.new_car = new_car
        super(RefuelForm, self).__init__(*args, **kwargs)
        self.fields['date'] = forms.DateTimeField(label='Date and Time', initial=timezone.now())
        if new_car:
            self.fields['odometer'] = forms.DecimalField(label="Total mileage (This is your vehicle's total mileage, \
                                                                not your journey mileage)")
            self.fields['full_tank'] = forms.ChoiceField(label="Did you fill the tank? (Full-tank refuels will give \
                                                                quicker results)",
                                                         choices=[(True, 'Yes. I filled the tank.'),
                                                                  (False, 'No. I partially filled the tank.')],
                                                         widget=forms.RadioSelect(),
                                                         required=True)

        else:
            self.fields['odometer'] = forms.DecimalField(label='Total mileage')
            self.fields['litres'] = forms.DecimalField(label='Litres of fuel', min_value=0.1, max_value=500)
            self.fields['price'] = forms.DecimalField(label='Price paid (£)', min_value=0.01, max_value=750)
            self.fields['full_tank'] = forms.ChoiceField(label="Did you fill the tank?",
                                                         choices=[(True, 'Yes. I filled the tank.'),
                                                                  (False, 'No. I partially filled the tank.')],
                                                         widget=forms.RadioSelect(),
                                                         required=True)

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

    def clean_date(self):
        date = self.cleaned_data['date']
        if not self.new_car:
            if date < self.date_validation:
                raise ValidationError(
                    "That pre-dates your last refuel (" + str(self.date_validation)[:19] + ")"
                )
            return date
        else:
            return date
