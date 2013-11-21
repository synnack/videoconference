"""
Django url dispatcher for the relative /scheduler/ URL to view mapping.
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

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'scheduler.views.list_reservations', name='reservations'),
    url(r'^reservation/(\d*)$', 'scheduler.views.edit_reservation', name='reservation'),
)
