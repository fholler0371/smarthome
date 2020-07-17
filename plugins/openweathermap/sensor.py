import json

known_sensors = {}

def new_value(name, value, last):
    global known_sensors
    if not(name in known_sensors):
        known_sensors[name] = {'friendly_name' : name, 'value' : str(value), 'seen': False, 'unit': '', 'type': '', 
                               'has_default': False, 'default': '', 'var_type': 'str', 'send': False}
#        print('New Sensor:', name)
    else:
        known_sensors[name]['value'] = value
#    print(name, value, last)

def load(sh):
#    try:
    if True:
        global known_sensors
        f = open(sh.const.path + '/db/openweathermap.json', 'r')
        known_sensors = json.loads(f.read())
        f.close()
#    except:
#        print('error')
#        pass

def save(sh):
    global known_sensors
    f = open(sh.const.path + '/db/openweathermap.json', 'w')
    f.write(json.dumps(known_sensors))
    f.close()
