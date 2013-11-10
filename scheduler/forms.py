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
