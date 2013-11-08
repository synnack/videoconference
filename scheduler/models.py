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
    mcu = models.ForeignKey(MCU)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    description  = models.TextField()
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participant_count = models.IntegerField(null=False)

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name
