
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

urlpatterns = [  # don't terminate with a $ when using includes
    url(r'^admin/', admin.site.urls),
    url(r'^', include('complementary_pages.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^forum/', include('forum.urls')),
    url(r'^cars/', include('cars.urls')),
    url(r'^stats/', include('stats.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
