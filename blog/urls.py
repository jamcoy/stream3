from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name="blog_post_list"),
    url(r'^blogTop5/$', views.top_posts, name="blog_top_posts"),
    url(r'^(?P<db_id>\d+)/$', views.post_detail, name="blog_post_detail"),
    url(r'^post/$', views.new_post, name='blog_new_post'),
    url(r'^(?P<db_id>\d+)/edit$', views.edit_post, name="blog_edit_post"),
]
