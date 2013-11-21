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
        methods = self.mcu.GetMosaicLayout()
        return methods
