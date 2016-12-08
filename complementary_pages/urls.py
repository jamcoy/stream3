from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^contact/$', views.contact),
    url(r'^about/$', views.about),
    url(r'^terms/$', views.terms),
]