from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'presider.views.ongoing_conferences', name='ongoing_conferences'),
    url(r'^conference/(\d*)$', 'presider.views.preside_over_conference', name='conference'),
    url(r'^ajax/(\d*)$', 'presider.views.ajax', name='ajax'),
)
