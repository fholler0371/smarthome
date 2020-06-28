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
