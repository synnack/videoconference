from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'scheduler.views.index', name='index'),
    url(r'^request/$', 'scheduler.views.request', name='request'),
    url(r'^rooms/$', 'scheduler.views.rooms', name='rooms'),
    url(r'^room/(\d*)$', 'scheduler.views.room', name='room'),
)
