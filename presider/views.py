from django.shortcuts import render, redirect
from scheduler.models import Reservation, MCU
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.http import HttpResponse
from presider import ajax as ajax_mod

@login_required
def ongoing_conferences(request):
    conferences = Reservation.objects.filter(user=request.user).filter(status="inprogress").order_by('begin_time')
    context = { 'conferences': conferences }

    return render(request, "presider/ongoing_conferences.html", context)

@login_required
def preside_over_conference(request, id):
    conference = Reservation.objects.get(id=id)
    if conference.user != request.user:
        return HttpResponse("Nope")

    context = { 'id': id }

    return render(request, "presider/preside_over_conference.html", context)


@login_required
def ajax(request,id):
    conference = Reservation.objects.get(id=id)
    if conference.user != request.user:
        return HttpResponse("Nope")

    # Get room information call: Not really, but FIXME
    response = ajax_mod.get_room_information('http://127.0.0.1:1420', 'room101')
    return HttpResponse(response)

