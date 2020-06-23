import plugins

class plugin(plugins.base):
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')
        self._create_config()
        self.require = ['webserver']
        self.get_requirements()
        print(self.cfg)

    def _create_config(self):
        self.sh.log.info('_create_config')
        change = False
        if not self.name in self.sh.cfg.data['plugins']:
            self.sh.cfg.data['plugins'][self.name] = {}
            change = True
        if not 'port' in self.sh.cfg.data['plugins'][self.name]:
            self.sh.cfg.data['plugins'][self.name]['port'] = 4100
            change = True
        if change:
             self.sh.cfg.save()
        self.cfg = self.sh.cfg.data['plugins'][self.name]
