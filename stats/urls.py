from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.stats),
]
