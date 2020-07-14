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

def load(self):
    print('openweather load data')

def save(self):
    print('openweather save data')
