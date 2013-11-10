from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'scheduler.views.list_reservations', name='reservations'),
    url(r'^reservation/(\d*)$', 'scheduler.views.edit_reservation', name='reservation'),
)
