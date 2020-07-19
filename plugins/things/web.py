def sm_backend(sh, plugin, data):
    if 'client_get_var' == data['data']['cmd']:
        data['data'] = get_var(plugin)
    elif 'client_set_var' == data['data']['cmd']:
        data['data'] = set_var(sh, plugin, data['data'])
    print(data)
    return data['data']

def get_var(plugin):
    out = {}
    out['friendly_name']= plugin.cfg['friendly_name']
    return out

def set_var(sh, plugin, data):
    plugin.cfg['friendly_name'] = data['friendly_name']
    sh.cfg.data['plugins'][plugin.name]['friendly_name'] = data['friendly_name']
    sh.cfg.save()
    return {}
