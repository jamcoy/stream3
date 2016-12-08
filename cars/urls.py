from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.list_cars, name='car_cars'),
    url(r'^(?P<car_id>\d+)/$', views.car_stats, name='car_stats'),
    url(r'^add_car/$', views.add_car, name='car_add'),
    url(r'^add_car_details/$', views.add_car_details, name='car_add_details'),
    url(r'^delete_car/(?P<car_id>\d+)/$', views.delete_car, name='car_delete'),
    url(r'^refuel_car/(?P<car_id>\d+)/$', views.refuel_car, name='car_refuel'),
    url(r'^refuel_history/(?P<car_id>\d+)/$', views.refuel_history, name='car_refuel_history'),
    url(r'^car_details/(?P<car_id>\d+)/$', views.car_details, name='car_details'),
    url(r'^upload_image/(?P<car_id>\d+)/$', views.upload_image, name='car_upload_image'),
    url(r'^select_chart/$', views.select_chart, name="car_select_chart"),
]
