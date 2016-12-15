# -*- coding: utf-8 -*-
from django.test import TestCase
from accounts.models import User
from .views import car_stats, car_details, refuel_history, upload_image, delete_car, refuel_car, add_car
from django.core.urlresolvers import resolve
from .models import Car, Refuel
from decimal import *
from django.utils import timezone
from datetime import timedelta
from .forms import RefuelForm


class CarTest(TestCase):

    def setUp(self):
        super(CarTest, self).setUp()

        self.user = User.objects.create(username='testing_user')
        self.user.set_password('pleaseletmein')
        self.user.save()
        self.login = self.client.login(username='testing_user',
                                       password='pleaseletmein')
        self.assertEqual(self.login, True)

        self.car = Car.objects.create(
            date_added="2016-12-14T15:19:25.219Z",
            exclude_from_collation=False,
            exclude_from_collation_reason="",
            make="FORD",
            model="FOCUS",
            sub_model="ZETEC 100",
            colour="BLUE",
            year_of_manufacture="2009",
            cylinder_capacity="1596 cc",
            transmission="MANUAL",
            fuel_type="PETROL",
            co2="159 g/km",
            doors="5",
            image="",
            user_id=self.user.id
        )
        self.car.save()

        self.refuel = Refuel.objects.create(
            date="2016-12-14T15:22:20Z",
            date_time_added="2016-12-14T15:23:02.230Z",
            litres="0.00",
            price="0.00",
            odometer="90351.00",
            full_tank=True,
            missed_refuels=True,
            car_id=self.car.id,
            user_id=self.user.id
        )
        self.refuel.save()

        self.refuel = Refuel.objects.create(
            date="2016-12-14T15:23:23Z",
            date_time_added="2016-12-14T15:23:43.964Z",
            litres="44.48",
            price="47.90",
            odometer="90726.00",
            full_tank=True,
            missed_refuels=False,
            car_id=self.car.id,
            user_id=self.user.id
        )
        self.refuel.save()

        self.refuel = Refuel.objects.create(
            date="2016-12-14T15:23:47Z",
            date_time_added="2016-12-14T15:24:07.778Z",
            litres="20.24",
            price="22.65",
            odometer="90904.00",
            full_tank=True,
            missed_refuels=False,
            car_id=self.car.id,
            user_id=self.user.id
        )
        self.refuel.save()

        self.param = str(self.car.pk) + "/"

    # car economy calculations test
    def test_check_calculation_values(self):
        response = self.client.get('/cars/' + self.param)
        self.assertEqual(response.context['car_statistic'], {'fuel_cost': 109.0, 'ppm': 12.8, 'miles': '553',
                                                             'expenditure': Decimal('70.55'), 'fuel': '65',
                                                             'economy': 38.8})

    # car_stats_unit_tests
    def test_car_stats_page_resolves(self):
        response = resolve('/cars/' + self.param)
        self.assertEqual(response.func, car_stats)

    def test_car_stats_status_code_is_ok(self):
        response = self.client.get('/cars/' + self.param)
        self.assertEqual(response.status_code, 200)

    def test_check_loads_correct_template(self):
        response = self.client.get('/cars/' + self.param)
        self.assertTemplateUsed(response, "cars/car_stats.html")

    def test_check_loads_content(self):
        response = self.client.get('/cars/' + self.param)
        self.assertContains(response, 'Larger points represent accumulated part-tank refuels')

    # car_details_unit_tests
    def test_car_details_page_resolves(self):
        response = resolve('/cars/car_details/' + self.param)
        self.assertEqual(response.func, car_details)

    def test_car_details_status_code_is_ok(self):
        response = self.client.get('/cars/car_details/' + self.param)
        self.assertEqual(response.status_code, 200)

    def test_check_details_correct_template(self):
        response = self.client.get('/cars/car_details/' + self.param)
        self.assertTemplateUsed(response, "cars/car_details.html")

    def test_check_details_content(self):
        response = self.client.get('/cars/car_details/' + self.param)
        self.assertContains(response, 'Contributing to community data')

    # refueling_history_unit_tests
    def test_refuel_history_page_resolves(self):
        response = resolve('/cars/refuel_history/' + self.param)
        self.assertEqual(response.func, refuel_history)

    def test_refuel_history_status_code_is_ok(self):
        response = self.client.get('/cars/refuel_history/' + self.param)
        self.assertEqual(response.status_code, 200)

    def test_refuel_history_correct_template(self):
        response = self.client.get('/cars/refuel_history/' + self.param)
        self.assertTemplateUsed(response, "cars/refuel_history.html")

    def test_refuel_history_content(self):
        response = self.client.get('/cars/refuel_history/' + self.param)
        # check contains concatenation of Make, model and sub-model
        self.assertContains(response, "See economy calculations below for details about what's included.")

    def test_refuel_history_number_of_entries(self):
        response = self.client.get('/cars/refuel_history/' + self.param)
        self.assertEqual(len(response.context['refuels']), 3)

    # upload_photo_unit_tests
    def test_car_upload_photo_page_resolves(self):
        response = resolve('/cars/upload_image/' + self.param)
        self.assertEqual(response.func, upload_image)

    def test_car_upload_photo_status_code_is_ok(self):
        response = self.client.get('/cars/upload_image/' + self.param)
        self.assertEqual(response.status_code, 200)

    def test_car_upload_photo_correct_template(self):
        response = self.client.get('/cars/upload_image/' + self.param)
        self.assertTemplateUsed(response, "cars/upload_image.html")

    def test_car_upload_photo_content(self):
        response = self.client.get('/cars/upload_image/' + self.param)
        self.assertContains(response, 'Upload a photo of your car')

    # upload_delete_car_unit_tests
    def test_car_delete_page_resolves(self):
        response = resolve('/cars/delete_car/' + self.param)
        self.assertEqual(response.func, delete_car)

    def test_car_delete_status_code_is_ok(self):
        response = self.client.get('/cars/delete_car/' + self.param)
        self.assertEqual(response.status_code, 200)

    def test_car_delete_correct_template(self):
        response = self.client.get('/cars/delete_car/' + self.param)
        self.assertTemplateUsed(response, "cars/delete_car.html")

    def test_car_delete_content(self):
        response = self.client.get('/cars/delete_car/' + self.param)
        # self.assertContains(response, 'BLUE 2009 FORD FOCUS ZETEC 100')
        self.assertContains(response, 'BLUE 2009 FORD FOCUS ZETEC 100')

    # Refuel_car_unit_tests
    def test_car_refuel_page_resolves(self):
        response = resolve('/cars/refuel_car/' + self.param)
        self.assertEqual(response.func, refuel_car)

    def test_car_refuel_status_code_is_ok(self):
        response = self.client.get('/cars/refuel_car/' + self.param)
        self.assertEqual(response.status_code, 200)

    def test_car_refuel_correct_template(self):
        response = self.client.get('/cars/refuel_car/' + self.param)
        self.assertTemplateUsed(response, "cars/refuel_car.html")

    def test_car_refuel_content(self):
        response = self.client.get('/cars/refuel_car/' + self.param)
        self.assertContains(response, 'Enter refueling details')

    # Add car_unit_tests
    def test_add_car_page_resolves(self):
        response = resolve('/cars/add_car/')
        self.assertEqual(response.func, add_car)

    def test_add_car_status_code_is_ok(self):
        response = self.client.get('/cars/add_car/')
        self.assertEqual(response.status_code, 200)

    def test_add_car_correct_template(self):
        response = self.client.get('/cars/add_car/')
        self.assertTemplateUsed(response, "cars/add_car.html")

    def test_add_car_content(self):
        response = self.client.get('/cars/add_car/')
        self.assertContains(response, 'Enter your registration')

    # test refuel form with valid data
    def test_refuel_form(self):
        form = RefuelForm({
            'date': timezone.now(),
            'odometer': 100000,
            'litres': 100,
            'price': 100,
            'full_tank': True,
            'missed_refuels': False},
            odometer_validation=90904,
            date_validation=timezone.now() - timedelta(days=1),
            skip_missed_refuel_question=False
        )
        self.assertTrue(form.is_valid())

    # test refuel form with an odometer that's less that a preceding mileage
    def test_refuel_form_mileage_less_than_preceding_mileage(self):
        form = RefuelForm({
            'date': timezone.now(),
            'odometer': 90800,
            'litres': 100,
            'price': 100,
            'full_tank': True,
            'missed_refuels': False},
            odometer_validation=90904,
            date_validation=timezone.now() - timedelta(days=1),
            skip_missed_refuel_question=False
        )
        self.assertFalse(form.is_valid())

    # test refuel form with a date that precedes the last refuel
    def test_refuel_form_date_preceded_preceding_date(self):
        form = RefuelForm({
            'date': timezone.now() - timedelta(days=1),
            'odometer': 100000,
            'litres': 100,
            'price': 100,
            'full_tank': True,
            'missed_refuels': False},
            odometer_validation=90904,
            date_validation=timezone.now(),
            skip_missed_refuel_question=False
        )
        self.assertFalse(form.is_valid())

    # test refuel form without an odometer reading
    def test_refuel_form_no_mileage_submitted(self):
        form = RefuelForm({
            'date': timezone.now(),
            'litres': 100,
            'price': 100,
            'full_tank': True,
            'missed_refuels': False},
            odometer_validation=90904,
            date_validation=timezone.now() - timedelta(days=1),
            skip_missed_refuel_question=False
        )
        self.assertFalse(form.is_valid())

    # test refuel from without a litre value
    def test_refuel_no_litre_value_submitted(self):
        form = RefuelForm({
            'date': timezone.now(),
            'odometer': 100000,
            'price': 100,
            'full_tank': True,
            'missed_refuels': False},
            odometer_validation=90904,
            date_validation=timezone.now() - timedelta(days=1),
            skip_missed_refuel_question=False
        )
        self.assertFalse(form.is_valid())

    # test refuel form without a price value
    def test_refuel_form_no_price_value_submitted(self):
        form = RefuelForm({
            'date': timezone.now(),
            'odometer': 100000,
            'litres': 100,
            'full_tank': True,
            'missed_refuels': False},
            odometer_validation=90904,
            date_validation=timezone.now() - timedelta(days=1),
            skip_missed_refuel_question=False
        )
        self.assertFalse(form.is_valid())

    # test refuel form with no answer to full_tank
    def test_refuel_full_tank_question_unanswered(self):
        form = RefuelForm({
            'date': timezone.now(),
            'odometer': 100000,
            'litres': 100,
            'price': 100,
            'missed_refuels': False},
            odometer_validation=90904,
            date_validation=timezone.now() - timedelta(days=1),
            skip_missed_refuel_question=False
        )
        self.assertFalse(form.is_valid())

    # test refuel form with no answer to missed_refuels
    def test_refuel_missed_refuels_question_unanswered(self):
        form = RefuelForm({
            'date': timezone.now(),
            'odometer': 100000,
            'litres': 100,
            'price': 100,
            'full_tank': True},
            odometer_validation=90904,
            date_validation=timezone.now() - timedelta(days=1),
            skip_missed_refuel_question=False
        )
        self.assertFalse(form.is_valid())
