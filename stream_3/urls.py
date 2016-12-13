
from django.conf.urls import include, url
from django.contrib import admin
from settings.base import MEDIA_ROOT, DEBUG
from django.views.static import serve

urlpatterns = [  # don't terminate with a $ when using includes
    url(r'^admin/', admin.site.urls),
    url(r'^', include('complementary_pages.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^forum/', include('forum.urls')),
    url(r'^cars/', include('cars.urls')),
    url(r'^stats/', include('stats.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
