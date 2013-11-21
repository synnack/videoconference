"""
Django database models specific to the scheduler.
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

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MCU(models.Model):
    TYPE_OPTIONS = (
        ("medooze", "Medooze"),
        ("openmcu-ru", "OpenMCU-ru")
    )
    name = models.CharField(max_length=60)
    hostname = models.CharField(max_length=200)
    mcu_type = models.CharField(max_length=25, choices=TYPE_OPTIONS, default="medooze")
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
    status = models.CharField(max_length=25, choices=STATUS_OPTIONS, default="planned")

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name
