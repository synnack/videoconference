"""
Django /presider/ views. See urls.py for relative dispatching from /presider/.
"""
#
# Copyright (C) by Wilco Baan Hofman <wilco@baanhofman.nl> 2013
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from django.shortcuts import render
from scheduler.models import Reservation
from django.contrib.auth.decorators import login_required
#from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponse

@login_required
def ongoing_conferences(request):
    conferences = Reservation.objects.filter(user=request.user).filter(status="inprogress").order_by('begin_time')
    context = { 'conferences': conferences }

    return render(request, "presider/ongoing_conferences.html", context)


@login_required
#@requires_csrf_token # Currently not necessary, due to redesign.
def preside_over_conference(request, id):
    conference = Reservation.objects.get(id=id)
    if conference.user != request.user:
        return HttpResponse("Nope")

    context = { 'id': id }

    return render(request, "presider/preside_over_conference.html", context)

