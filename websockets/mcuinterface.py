"""
Websocket MCU backend interface. Defines the interface as used by Medooze/OpenMCU-ru
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

class MCUInterface():
    """
    This is a base class for multiple MCU backends.
    """

    def list_participants():
        raise NotImplementedError("This method was not implemented by this backend")
    def move_participant():
        raise NotImplementedError("This method was not implemented by this backend")
    def remove_participant():
        raise NotImplementedError("This method was not implemented by this backend")
    def disable_audio_participant():
        raise NotImplementedError("This method was not implemented by this backend")
    def enable_audio_participant():
        raise NotImplementedError("This method was not implemented by this backend")
    def disable_video_participant():
        raise NotImplementedError("This method was not implemented by this backend")
    def enable_video_participant():
        raise NotImplementedError("This method was not implemented by this backend")
    def list_mosaic_positions():
        raise NotImplementedError("This method was not implemented by this backend")
    def list_mosaics():
        raise NotImplementedError("This method was not implemented by this backend")
    def set_mosaic():
        raise NotImplementedError("This method was not implemented by this backend")
