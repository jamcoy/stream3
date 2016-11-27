from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Car(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    colour = models.CharField(max_length=20)
    year_of_manufacture = models.CharField(max_length=4)
    cylinder_capacity = models.CharField(max_length=6)
    transmission = models.CharField(max_length=10)
    fuel_type = models.CharField(max_length=10)
    co2 = models.CharField(max_length=10)
    doors = models.IntegerField
    total_fuel_litres = models.DecimalField  # fuelLitres
    total_fuel_expenditure = models.DecimalField  # fuelExpenditure
    total_mileage_tracked = models.DecimalField  # mileageTracked
    refuels = models.IntegerField
    economy_average = models.DecimalField  # "Need two refuels to calculate"
    economy_latest = models.DecimalField  # "Need two refuels to calculate"
    fuel_price_average = models.DecimalField  # "Need two refuels to calculate"  litrePriceAverage
    pence_per_mile_average = models.DecimalField  # "Need two refuels to calculate"
    dateAdded = models.DateTimeField(auto_now_add=True)
