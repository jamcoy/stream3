from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.economy_stats),
    url(r'^select_model/$', views.select_model, name="select_model"),
    url(r'^select_year/$', views.select_year, name="select_year"),
    url(r'^select_sub_details/$', views.select_sub_details, name="select_sub_details"),
]
