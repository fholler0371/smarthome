def sm_backend(sh, plugin, data):
    if 'client_get_var' == data['data']['cmd']:
        data['data'] = get_var(plugin)
    elif 'client_set_var' == data['data']['cmd']:
        data['data'] = set_var(sh, plugin, data['data'])
    return data['data']

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
