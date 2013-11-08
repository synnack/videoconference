from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'scheduler.views.reservations', name='reservations'),
    url(r'^reservation/(\d*)$', 'scheduler.views.reservation', name='reservation'),
)
