from django.shortcuts import render, redirect
from scheduler.forms import ReservationForm
from scheduler.models import Reservation, MCU
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ValidationError

def index(request):
    return render(request, "sorry.html")

def conference(request, id):
    return render(request, "sorry.html")


def ajax(request):
    return render(request, "sorry.html")
