from threading import Thread, Timer

import plugins

class plugin(plugins.base):
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')
        val = {}
        self.create_config(val)
        self.loaded = True
        if self.loaded:
            self.sh.plugins.register(self)
