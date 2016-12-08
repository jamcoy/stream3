from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.forum, name='forum_forums'),
    url(r'^threads/(?P<subject_id>\d+)/$', views.threads, name='forum_threads'),
    url(r'^new_thread/(?P<subject_id>\d+)/(?P<poll>\w+)/$', views.new_thread, name='forum_new_thread'),
    url(r'^thread/(?P<thread_id>\d+)/$', views.thread, name='forum_thread'),
    url(r'^post/new/(?P<thread_id>\d+)/$', views.new_post, name='forum_'),
    url(r'^post/edit/(?P<thread_id>\d+)/(?P<post_id>\d+)/$', views.edit_post, name='forum_'),
    url(r'^post/delete/(?P<thread_id>\d+)/(?P<post_id>\d+)/$', views.delete_post, name='forum_'),
    url(r'^thread/vote/(?P<thread_id>\d+)/(?P<subject_id>\d+)/$', views.thread_vote, name='forum_'),
]
