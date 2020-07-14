import plugins.openweathermap.sensor as sensor

def sm_backend(sh, plugin, data):
    if 'client_get_var' == data['data']['cmd']:
        data['data'] = get_var(plugin)
    elif 'client_set_var' == data['data']['cmd']:
        data['data'] = set_var(sh, plugin, data['data'])
    elif 'client_get_sensor' == data['data']['cmd']:
        data['data'] = get_sensor()
    return data['data']

def get_sensor():
   out = []
   for name in sensor.known_sensors:
       data = sensor.known_sensors[name]
       data['name'] = name
       out.append(data)
   return {'sensors': out}

def set_var(sh, plugin, data):
   plugin.cfg['friendly_name'] = data['friendly_name']
   sh.cfg.data['plugins'][plugin.name]['friendly_name'] = data['friendly_name']
   plugin.cfg['api'] = data['api']
   sh.cfg.data['plugins'][plugin.name]['api'] = data['api']
   plugin.cfg['intervall'] = data['intervall']
   sh.cfg.data['plugins'][plugin.name]['intervall'] = data['intervall']
   sh.cfg.save()
   return {}

def get_var(plugin):
   out = {}
   out['friendly_name']= plugin.cfg['friendly_name']
   out['api']= plugin.cfg['api']
   out['intervall']= plugin.cfg['intervall']
   return out
