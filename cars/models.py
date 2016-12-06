from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from stdimage.models import StdImageField


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
    doors = models.CharField(max_length=2)
    image = StdImageField(upload_to="images/cars",
                          variations={
                              'large': {'width': 960, 'height': 640},
                              'medium': {'width': 360, 'height': 240},
                              'thumbnail': {'width': 120, 'height': 80, "crop": True}
                          },
                          blank=True, null=True)

    def __str__(self):
        return self.make + " " \
             + self.model + " " \
             + self.sub_model \
             + " " \
             + self.year_of_manufacture


class Refuel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    car = models.ForeignKey(Car)
    date = models.DateTimeField(null=True)
    date_time_added = models.DateTimeField(auto_now_add=True)
    litres = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    odometer = models.DecimalField(max_digits=12, decimal_places=2)
    full_tank = models.BooleanField()
    missed_refuels = models.BooleanField()

    def __str__(self):
        if self.full_tank:
            tank = "Full tank"
        else:
            tank = "Partial refuel"
        return str(self.date) + ", Odometer: " \
             + str(self.odometer) + " miles, " \
             + str(self.litres) + " litres, " \
             + str(self.price) + " GBP, " \
             + tank

