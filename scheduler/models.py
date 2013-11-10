from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MCU(models.Model):
    name = models.CharField(max_length=60)
    hostname = models.CharField(max_length=200)
    sip_port = models.IntegerField()
    http_port = models.IntegerField()

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name


class Reservation(models.Model):
    STATUS_OPTIONS = (
        ("planned", "Planned"),
        ("inprogress", "In progress"),
        ("done", "Done")
    )
    mcu = models.ForeignKey(MCU)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    description  = models.TextField()
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participant_count = models.IntegerField(null=False)
    status = models.CharField(max_length=25, choices=STATUS_OPTIONS, default="planned") # This is really one choice with multiple options. Dafuq?

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name
