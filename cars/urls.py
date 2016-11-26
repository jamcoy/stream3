from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.cars),
    url(r'^add_car/$', views.add_car),
    url(r'^add_car_details/$', views.add_car_details),
]
