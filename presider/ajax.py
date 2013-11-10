import simplejson as json
import requests

def get_room_information(mcu, room):
    r = requests.post(mcu + "/Select", data={'room': room, 'opts': ''})
    try:
        print r.text
        conf = r.json()['conf']
    except Exception as e:
        print e
        return "{}"


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

    return json.dumps(conf_info)
