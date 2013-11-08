from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'videoconference.views.index', name='index'),
    url(r'^scheduler/', include('scheduler.urls', namespace='scheduler')),
    url(r'^presider/', include('presider.urls', namespace='presider')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
