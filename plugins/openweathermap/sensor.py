import json

known_sensors = {}
sh = None
things = None
plugin = None

def new_value(name, value, last):
    global known_sensors
    global things, plugin
    if not(name in known_sensors):
        known_sensors[name] = {'friendly_name' : name, 'value' : str(value), 'seen': False, 'unit': '', 'type': '', 
                               'has_default': False, 'default': '', 'var_type': 'Str', 'send': False}
    else:
        known_sensors[name]['value'] = value
    if known_sensors[name]['send']:
        if 'Float' == known_sensors[name]['var_type']:
             value = float(value)
        elif 'Int' == known_sensors[name]['var_type']:
             value = int(float(value))
        things.new_sensor_value({'name': plugin.name+'|'+name,
               'friendly_name': plugin.cfg['friendly_name']+'/'+known_sensors[name]['friendly_name'],
               'value': value,
               'last': last,
               'unit': known_sensors[name]['unit'],
               'type': known_sensors[name]['type'],
               'var_type': known_sensors[name]['var_type']})

def set_row(data):
    global known_sensors
    if data['name'] in known_sensors:
        known_sensors[data['name']]['friendly_name'] = data['friendly_name']
        known_sensors[data['name']]['seen'] = data['seen']
        known_sensors[data['name']]['unit'] = data['unit']
        known_sensors[data['name']]['type'] = data['type']
        known_sensors[data['name']]['has_default'] = data['has_default']
        known_sensors[data['name']]['type'] = data['type']
        known_sensors[data['name']]['send'] = data['send']
        known_sensors[data['name']]['var_type'] = data['var_type']

def load(_sh, _plugin, _things):
    global known_sensors
    global sh
    global things
    global plugin
    things = _things
    sh = _sh
    plugin = _plugin
    print(sh)
    print(things)
    try:
        f = open(sh.const.path + '/db/openweathermap.json', 'r')
        known_sensors = json.loads(f.read())
        f.close()
    except Exception as e:
        sh.log.error(str(e))

def save(sh):
    global known_sensors
    f = open(sh.const.path + '/db/openweathermap.json', 'w')
    f.write(json.dumps(known_sensors))
    f.close()
