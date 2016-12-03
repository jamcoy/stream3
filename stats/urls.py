from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.economy_stats),
    url(r'^select_model/$', views.select_model, name="anything"),
    url(r'^select_year/$', views.select_year, name="anything else"),
    # url(r'^apply_filters/$', views.apply_filters, name="anything"),
]
