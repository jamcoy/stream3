from django.conf.urls import url
from . import views  # can probably shorten to import views

urlpatterns = [
    url(r'^$', views.forum, name='forum_forums'),
    url(r'^topics/(?P<subject_id>\d+)/$', views.threads, name='forum_threads'),
    url(r'^new_topic/(?P<subject_id>\d+)/(?P<poll>\w+)/$', views.new_thread, name='forum_new_thread'),
    url(r'^topic/(?P<thread_id>\d+)/$', views.thread, name='forum_thread'),
    url(r'^post/new/(?P<thread_id>\d+)/$', views.new_post, name='forum_new_post'),
    url(r'^post/edit/(?P<thread_id>\d+)/(?P<post_id>\d+)/$', views.edit_post, name='forum_edit_post'),
    url(r'^post/delete/(?P<post_id>\d+)/$', views.delete_post, name='forum_delete_post'),
    url(r'^topic/vote/(?P<thread_id>\d+)/(?P<subject_id>\d+)/$', views.thread_vote, name='forum_cast_vote'),
]
