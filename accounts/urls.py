from django.conf.urls import url
from . import views

urlpatterns = [

    # user accounts
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    # stripe
    url(r'^cancel_subscription/$', views.cancel_subscription, name='cancel_subscription'),
    url(r'^subscriptions_webhook/$', views.subscriptions_webhook, name='subscriptions_webhook'),

]