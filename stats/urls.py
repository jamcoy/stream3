from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.economy_stats),
    url(r'^test_ajax/$', views.test_ajax, name="anything"),
]
