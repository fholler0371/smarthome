import plugins.things.sensor as sensor

def sm_backend(sh, plugin, data):
    if 'client_get_var' == data['data']['cmd']:
        data['data'] = get_var(plugin)
    elif 'client_set_var' == data['data']['cmd']:
        data['data'] = set_var(sh, plugin, data['data'])
    elif 'client_get_sensor' == data['data']['cmd']:
        data['data'] = get_sensor(sh)
    print(data)
    return data['data']

def get_sensor(sh):
   out = []
   for name in sensor.sensors:
       data = sensor.sensors[name]
       data['name'] = name
       out.append(data)
   return {'sensors': out}

def get_var(plugin):
    out = {}
    out['friendly_name']= plugin.cfg['friendly_name']
    return out

def set_var(sh, plugin, data):
    plugin.cfg['friendly_name'] = data['friendly_name']
    sh.cfg.data['plugins'][plugin.name]['friendly_name'] = data['friendly_name']
    sh.cfg.save()
    return {}
