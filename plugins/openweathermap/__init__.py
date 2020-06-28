import plugins

class plugin(plugins.base):
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')
        self.require = ['timer']
        self.get_requirements()
        if self.loaded:
            self.sh.plugins.register(self)
        val = {
            'api' : '',
            'intervall' : 1200
          }
        self.create_config(val)

    def _set_config(self, data):
        self.cfg['api'] = data['api']
        self.cfg['intervall'] = data['intervall']
        self.sh.cfg.data['plugins'][self.name]['api'] = data['api']
        self.sh.cfg.data['plugins'][self.name]['intervall'] = data['intervall']
        self.sh.cfg.save()

    def webserver_api(self, data):
        cmd = data['cmd'].split('.')[2]
        if cmd == "get_config":
            return  {'api': self.cfg['api'], 'intervall': self.cfg['intervall']}
        elif cmd == "set_config":
            self._set_config(data)
            return  {}
        else:
            print(cmd)
        return data
