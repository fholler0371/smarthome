sensors = {}

sh = None
plugin = None

def new_value(data):
    global sensors
    if not(data['name'] in sensors):
        sensors[data['name']] = {'name': data['name'],
                                 'friendly_name': data['friendly_name'],
                                 'last_value': None,
                                 'value': None,
                                 'last_time': data['last'],
                                 'time': data['last'],
                                 'unit': data['unit'],
                                 'type': data['type'],
                                 'var_type': data['var_type']
                                 }
    change = False
    if data['value'] != sensors[data['name']]['value']:
        sensors[data['name']]['last_value'] = sensors[data['name']]['value']
        if sensors[data['name']]['last_value'] == None:
            sensors[data['name']]['last_value'] = data['value']
        sensors[data['name']]['last_time'] = sensors[data['name']]['time']
        change = True
    sensors[data['name']]['value'] = data['value']
    sensors[data['name']]['time'] = data['last']
    sensors[data['name']]['unit'] = data['unit']
    sensors[data['name']]['type'] = data['type']
    sensors[data['name']]['var_type'] = data['var_type']
#    print(sensors[data['name']])
#    print(change)

def load(_sh, _plugin):
    global sh, plugin
    sh = _sh
    plugin = _plugin
