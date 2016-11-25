from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.post_list, name="post_list"),
    url(r'^blogTop5/$', views.top_posts,),
    url(r'^(?P<db_id>\d+)/$', views.post_detail, name="post_list"),
    url(r'^post/$', views.new_post, name='new_post'),
    url(r'^(?P<db_id>\d+)/edit$', views.edit_post),
]
