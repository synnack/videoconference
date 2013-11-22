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

    def list_mosaic(self, data):
        methods = self.mcu.GetMosaicLayout(466419712, 0)

        if not 'returnVal' in methods:
            return {}

        positions = []
        for value in methods['returnVal'][0]['Positions']:
            positions.append({
                'pos_x': value['Left'],
                'pos_y': value['Top'],
                'width': value['Width'],
                'height': value['Height'],
            })

        return {
            'width': methods['returnVal'][0]['Width'],
            'height': methods['returnVal'][0]['Height'],
            'positions': positions
        }

    def move_participant(self, data):
        self.mcu.SetMosaicSlot(466419712, 0, int(data['target']), 503)
        self.mcu.SetMosaicSlot(466419712, 0, int(data['position']), 0)


    def remove_participant(self, data):
        self.mcu.SetMosaicSlot(466419712, 0, int(data['position']), 0)
