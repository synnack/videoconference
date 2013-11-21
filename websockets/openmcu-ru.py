"""
Websocket OpenMCU-ru backend. Communicates with the OpenMCU-ru MCU... sorta
"""
#
# Copyright (C) by Wilco Baan Hofman <wilco@baanhofman.nl> 2013
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import requests

class OpenMCUru(MCUInterface):
    """
    Interface to the OpenMCU-ru HTTP POST or whatever backend.
    """
    # These actions correspond to h323.h in OpenMCU-ru
    ACTIONS = {
        'OTFC_UNMUTE':                   0,
        'OTFC_MUTE':                     1,
        'OTFC_MUTE_ALL':                 2,
        'OTFC_REMOVE_FROM_VIDEOMIXERS':  3,
        'OTFC_REFRESH_VIDEO_MIXERS':     4,
        'OTFC_DROP_MEMBER':              7,
        'OTFC_VAD_NORMAL':               8,
        'OTFC_VAD_CHOSEN_VAN':           9,
        'OTFC_VAD_DISABLE_VAD':         10,
        'OTFC_REMOVE_VMP':              11,
        'OTFC_MOVE_VMP':                12,
        'OTFC_SET_VMP_STATIC':          13,
        'OTFC_VAD_CLICK':               14,
        'OTFC_MIXER_ARRANGE_VMP':       15,
        'OTFC_MIXER_SCROLL_LEFT':       16,
        'OTFC_MIXER_SHUFFLE_VMP':       17,
        'OTFC_MIXER_SCROLL_RIGHT':      18,
        'OTFC_MIXER_CLEAR':             19,
        'OTFC_MIXER_REVERT':            20,
        'OTFC_GLOBAL_MUTE':             21,
        'OTFC_SET_VAD_VALUES':          22,
        'OTFC_TEMPLATE_RECALL':         23,
        'OTFC_SAVE_TEMPLATE':           24,
        'OTFC_DELETE_TEMPLATE':         25,
        'OTFC_INVITE':                  32,
        'OTFC_REMOVE_OFFLINE_MEMBER':   33,
        'OTFC_DROP_ALL_ACTIVE_MEMBERS': 64,
        'OTFC_INVITE_ALL_INACT_MMBRS':  65,
        'OTFC_REMOVE_ALL_INACT_MMBRS':  66,
        'OTFC_SAVE_MEMBERS_CONF':       67,
        'OTFC_YUV_FILTER_MODE':         68,
        'OTFC_TAKE_CONTROL':            69,
        'OTFC_DECONTROL':               70,
        'OTFC_ADD_VIDEO_MIXER':         71,
        'OTFC_DELETE_VIDEO_MIXER':      72,
        'OTFC_SET_VIDEO_MIXER_LAYOUT':  73,
        'OTFC_SET_MEMBER_VIDEO_MIXER':  74,
        'OTFC_VIDEO_RECORDER_START':    75,
        'OTFC_VIDEO_RECORDER_STOP':     76,
    }


    def remove_participant(self, data):
        post = {
            'room':self.backend_info['room'],
            'otfc': 1,
            'action': self.ACTIONS['OTFC_REMOVE_VMP'],
            'v': 0, 
            'o': data['position'],
        }

        r = requests.post("http://" + self.backend_info['mcu'] + ":1420/Select", data=post)
        try:
            print r.text
            conf = r.json()['conf']
        except Exception as e:
            pass # This thing does not do JSON yet
            #return {'status': 'error', 'text': repr(e)}



    def move_participant(self, data):
        post = {
            'room':self.backend_info['room'],
            'otfc': 1,
            'action': self.ACTIONS['OTFC_MOVE_VMP'],
            'v': 0, 
            'o': data['position'],
            'o2': 0,                # Unknown what this does.
            'o3': data['target'],
        }

        r = requests.post("http://" + self.backend_info['mcu'] + ":1420/Select", data=post)
        try:
            print r.text
            conf = r.json()['conf']
        except Exception as e:
            pass # This thing does not do JSON yet
            #return {'status': 'error', 'text': repr(e)}


    def list_participants(self, data):
        self.sockets.send_local('NOTIFY_ERROR', { 'text': "LIST_PARTICIPANTS not implemented." }) # FIXME

    def get_conference_information(self, data):

        r = requests.post("http://" +self.backend_info['mcu'] + ":1420/Select", data={'room': self.backend_info['room'], 'opts': ''})
        try:
            print r.text
            conf = r.json()['conf']
        except Exception as e:
            self.sockets.send_local('NOTIFY_ERROR', { 'text': repr(e) })


        conf_info = {
            'mixer_count': conf[0][0],
            'frame_width': conf[0][1],
            'frame_height': conf[0][2],
            'room_name': conf[0][3],
            'control': True if conf[0][4] == '+' else False,
            'global_mute': True if conf[0][5] == '1' else False,
            'vad_level': conf[0][6],
            'vad_delay': conf[0][7],
            'vad_timeout': conf[0][8],
            'yuv_resizer_filter': conf[0][10],
            'external_recorder': True if conf[0][11] == '1' else False
        }

        if conf[0][10] == '1':
            conf_info['yuv_resizer_filter'] = True
        elif conf[0][10] == '0':
            conf_info['yuv_resizer_filter'] = False
        else:
            conf_info['yuv_resizer_filter'] = None

        conf_info['rooms'] = []
        for room in conf[0][9]:
            conf_info['rooms'].append({
                'room_name': room[0],
                'member_count': room[1],
                'is_moderated': True if room[2] == '+' else False,
            })

        conf_info['mixers'] = []
        for mixer in conf[1:]:
            mixer_info = {
                'mockup_width': mixer[0][0],
                'mockup_height': mixer[0][1],
                'layout': mixer[0][2],
            }
            mixer_info['frames'] = []
            for frame in mixer[1]:
                mixer_info['frames'].append({
                    'pos_x': frame[0],
                    'pos_y': frame[1],
                    'width': frame[2],
                    'height': frame[3],
                });

            mixer_info['members'] = {}
            for n, id in mixer[2].iteritems():
                mixer_info['members'][n] = {
                    'id': id,
                }
            for n, type in mixer[3].iteritems():
                mixer_info['members'][n]['type'] = (None, 'static', 'vad_normal', 'vad_chosen_van')[type]

            conf_info['mixers'].append(mixer_info)

        self.sockets.send_local("NOTIFY_CONFERENCE_INFO", conf_info)

