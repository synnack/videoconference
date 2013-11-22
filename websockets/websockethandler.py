"""
Websocket handler/dispatcher. Allows for realtime event-based communication.
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

import simplejson as json
import re

from websockets.medoozemcu import MedoozeMCU
from websockets.sip import SIP
"""
<?xml version="1.0" encoding="UTF-8"?>
<methodCall>
    <methodName>SetMosaicSlot</methodName>
    <params>
        <param><value><i4>466419712</i4></value></param>
        <param><value><i4>0</i4></value></param>
        <param><value><i4>4</i4></value></param>
        <param><value><i4>502</i4></value></param>
    </params>
</methodCall>
"""

class Handler():
    def __init__(self, backend_info, conference, sockets):
        self.backend_info = backend_info
        self.conference = conference
        self.sockets = sockets

    # Public methods
    def offer_sdp(self, data):
        sip = SIP('127.0.0.1', 'room101') # FIXME!!
        sip.bind('trying', self._sip_trying)
        sip.bind('ringing', self._sip_ringing)
        sip.bind('invite_ok', self._sip_invite_ok)
        sip.bind('media-error', self._sip_media_error)
        sip.bind('other', self._sip_other)

        self.sockets.add_sip(sip)

        sip.send_invite(data['sdp'])

    def sdp_ok(self, data):
        self.sockets.sip_connections[self.sockets.local].send_ack()

    def list_mosaic(self, data):
        mcu = MedoozeMCU('127.0.0.1')
        ret = mcu.list_mosaic(data)

        self.sockets.send_local("NOTIFY_MOSAIC", ret)

    def move_participant(self, data):
        if data['position'] == data['target']:
            # Well, that was easy
            return

        mcu = MedoozeMCU('127.0.0.1')
        ret = mcu.move_participant(data)


        self.sockets.send_conference("NOTIFY_PARTICIPANT_MOVE", ret)

    def remove_participant(self, data):
        mcu = MedoozeMCU('127.0.0.1')
        ret = mcu.remove_participant(data)

        self.sockets.send_conference("NOTIFY_PARTICIPANT_REMOVE", ret)

    # Private methods
    def _sip_trying(self, headers, body):
        self.sockets.send_local('NOTIFY_STATUS', { 'text': 'Trying...' })

    def _sip_ringing(self, headers, body):
        self.sockets.send_local('NOTIFY_STATUS', { 'text': 'Ringing...' })

    def _sip_invite_ok(self, headers, body):
        # Not sure what is required for FireFox.. but at least it doesn't like these attributes
        body = re.sub(r"\na=(extmap|ssrc|ice-lite).*\r", "", body, 0)
        self.sockets.send_local('OFFER_SDP', { 'sdp': body })

    def _sip_media_error(self, headers, body):
        self.sockets.send_local('NOTIFY_ERROR', { 'text': "Unsupported Media Type.." })

    def _sip_other(self, headers, body):
        self.sockets.send_local('NOTIFY_ERROR', { 'text': "Weird status received.." })


