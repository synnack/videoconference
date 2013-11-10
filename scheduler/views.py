from django.shortcuts import render, redirect
from scheduler.forms import ReservationForm
from scheduler.models import Reservation, MCU
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from datetime import datetime, timedelta

@login_required
def list_reservations(request):
    """
    Presents a list of reservations for this user ordered by date.
    """
    now = datetime.now() + timedelta(minutes=15)
    future_reservations = Reservation.objects.filter(user=request.user).filter(begin_time__gt=now).order_by('-begin_time')
    historical_reservations = Reservation.objects.filter(user=request.user).filter(begin_time__lte=now).order_by('-begin_time')

    context = { 
        'future_reservations': future_reservations,
        'historical_reservations': historical_reservations,
    }
    return render(request, 'scheduler/reservations.html', context)

@login_required
def edit_reservation(request, id):
    """
    Modify, cancel or create a reservation
    
    GET presents a form, POST updates the database
    If id is absent: create a new reservation
    If id is provided and also POST['cancel'], cancel a reservation
    If id is provided: modify a reservation
    """

    if not id:
        reservation = Reservation()
    else:
        reservation = Reservation.objects.get(id=id)
        if reservation == None or reservation.user != request.user:
            return HtmlResponse("Nope")

    form = None
    if request.POST:
        if id and 'cancel' in request.POST:
            # Cancel the reservation
            reservation.delete();
            return redirect(to=reverse('scheduler:reservations'))

        reservation.user = request.user
        reservation.mcu = MCU.objects.get(id=1)
        form = ReservationForm(request.POST, instance=reservation)
        try:
            form.save()
        except (ValueError, ValidationError) as e:
            # FIXME: Grab the error and show it to the user
            pass
        else:
            return redirect(to=reverse('scheduler:reservations'))

    if not form:
        form = ReservationForm(instance=reservation)

    context = { 'reservation': reservation, 'form': form }
    return render(request, 'scheduler/reservation.html', context)
