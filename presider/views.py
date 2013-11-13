from django.shortcuts import render, redirect
from scheduler.models import Reservation, MCU
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.http import HttpResponse
from presider.ajax import Ajax
import simplejson as json

@login_required
def ongoing_conferences(request):
    conferences = Reservation.objects.filter(user=request.user).filter(status="inprogress").order_by('begin_time')
    context = { 'conferences': conferences }

    return render(request, "presider/ongoing_conferences.html", context)


@login_required
@requires_csrf_token
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
        return HttpResponse("{}")

    # FIXME Hardcoded
    backend_info = {
            'mcu': 'http://127.0.0.1:1420',
            'room': 'room101',
    }

    ajax = Ajax(backend_info=backend_info, conference=conference)

    actions = {
            'GET_CONFERENCE_INFO':   'get_conference_information',
            'LIST_PARTICIPANTS':     'list_participants',
            'MOVE_PARTICIPANT':      'move_participant',
            'REMOVE_PARTICIPANT':    'remove_participant',
    }

    if not 'action' in request.POST or not request.POST['action'] in actions:
        return HttpResponse("{}")

    # Find and call the method in the ajax class instance
    func = getattr(ajax, actions[request.POST['action']])
    response = func(request.POST)

    return HttpResponse(json.dumps(response))

