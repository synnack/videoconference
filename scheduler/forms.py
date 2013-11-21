"""
Django form for reserving a conference and editing a conference reservation.
"""

__copyright__ = """
Copyright (C) by Wilco Baan Hofman <wilco@baanhofman.nl> 2013

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from scheduler.models import Reservation

from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets

class ReservationForm(ModelForm):
    participant_count = forms.IntegerField(widget=forms.Select(choices=[('','')]+[(i,i) for i in range(3,22)]))

    class Meta:
        model = Reservation
        fields = ['name', 'begin_time', 'end_time', 'participant_count', 'description']
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['end_time'].widget = widgets.AdminSplitDateTime()
        self.fields['begin_time'].widget = widgets.AdminSplitDateTime()
