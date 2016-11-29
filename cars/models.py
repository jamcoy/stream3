from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Car(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_added = models.DateTimeField(auto_now_add=True)
    exclude_from_collation = models.BooleanField(default=False)
    exclude_from_collation_reason = models.CharField(max_length=30, null=True)

    # vehicle details
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    sub_model = models.CharField(max_length=30, null=True)
    colour = models.CharField(max_length=20)
    year_of_manufacture = models.CharField(max_length=10)
    cylinder_capacity = models.CharField(max_length=10)
    transmission = models.CharField(max_length=10)
    fuel_type = models.CharField(max_length=10)
    co2 = models.CharField(max_length=10)
    doors = models.CharField(max_length=10)

    # figures from first refill. Data from sign-up to first refill is NOT used, since user may not no what's in the tank
    mileage_initial = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    fuel_litres_initial = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # fuelLitres
    fuel_expenditure_initial = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # totals for what's been tracked
    mileage_tracked = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # mileageTracked
    fuel_litres_tracked = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # fuelLitres
    fuel_expenditure_tracked = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # fuelExpenditure

    refuels = models.IntegerField(default=0)
    mileage_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # mileage
    mileage_previous = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # calculations (these could be calculated live instead of storing, but this will speed up browsing collated figures
    economy_average = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # "Need two refuels to calculate"
    economy_latest = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # "Need two refuels to calculate"
    fuel_price_average = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # "Need two refuels to calculate"  litrePriceAverage
    price_per_mile_average = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # "Need two refuels to calculate"


    def __str__(self):
        return self.make + " " + self.model + " " + self.year_of_manufacture
