from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Car(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    colour = models.CharField(max_length=20)
    year_of_manufacture = models.CharField(max_length=10)
    cylinder_capacity = models.CharField(max_length=10)
    transmission = models.CharField(max_length=10)
    fuel_type = models.CharField(max_length=10)
    co2 = models.CharField(max_length=10)
    doors = models.CharField(max_length=10)
    total_fuel_litres = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # fuelLitres
    total_fuel_expenditure = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # fuelExpenditure
    total_mileage_tracked = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # mileageTracked
    refuels = models.IntegerField(default=0)
    economy_average = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # "Need two refuels to calculate"
    economy_latest = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # "Need two refuels to calculate"
    fuel_price_average = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # "Need two refuels to calculate"  litrePriceAverage
    price_per_mile_average = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # "Need two refuels to calculate"
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.make + " " + self.model + " " + self.year_of_manufacture
