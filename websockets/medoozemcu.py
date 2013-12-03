"""
Websocket Medooze MCU backend. Handles communication with the Medooze MCU.
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

import xmlrpclib
from mcuinterface import MCUInterface

class MedoozeMCU(MCUInterface):
    """
    Interface to the Medooze MCU XMLRPC backend.
    """
    def __init__(self, hostname):
        self.mcu = xmlrpclib.ServerProxy("http://127.0.0.1:8085/mcu/mcu")
        self.conference = 2002649088

    def list_mosaic(self, data):
        layout = self.mcu.GetMosaicLayout(self.conference, 0)

        print layout

        if layout['returnCode'] == 0:
            if layout['errorMsg'] == "Conference does not exist":
                val = self.mcu.CreateConference("87bcc0c1-4ec3-46ea-9b2e-63e9c740f5c7", 0, 0, 8000)
                print val['returnVal'][0]
                self.conference = val['returnVal'][0]
                layout = self.mcu.GetMosaicLayout(self.conference, 0)
            else:
                return {}

        print layout
        if not 'returnVal' in layout:
            return {}

        positions = []
        for value in layout['returnVal'][0]['Positions']:
            positions.append({
                'pos_x': value['Left'],
                'pos_y': value['Top'],
                'width': value['Width'],
                'height': value['Height'],
            })

        return {
            'width': layout['returnVal'][0]['Width'],
            'height': layout['returnVal'][0]['Height'],
            'positions': positions
        }

    def move_participant(self, data):
        self.mcu.SetMosaicSlot(self.conference, 0, int(data['target']), 502)
        self.mcu.SetMosaicSlot(self.conference, 0, int(data['position']), 0)

        return { 'position': data['position'], 'target': data['target'] }

    def remove_participant(self, data):
        self.mcu.SetMosaicSlot(self.conference, 0, int(data['position']), 0)

        return { 'position': data['position'] }

    def list_participants(self, data):
        obj = self.mcu.ListParticipants(self.conference, 0)

        return obj
