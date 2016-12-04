from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.list_cars),
    url(r'^(?P<car_id>\d+)/$', views.car_stats),
    url(r'^add_car/$', views.add_car),
    url(r'^add_car_details/$', views.add_car_details),
    url(r'^delete_car/(?P<car_id>\d+)/$', views.delete_car),
    url(r'^refuel_car/(?P<car_id>\d+)/$', views.refuel_car),
    url(r'^refuel_history/(?P<car_id>\d+)/$', views.refuel_history),
    url(r'^car_details/(?P<car_id>\d+)/$', views.car_details),
    url(r'^upload_image/(?P<car_id>\d+)/$', views.upload_image),
    url(r'^select_chart/$', views.select_chart, name="select_chart"),
]
