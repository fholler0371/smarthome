import os

import importlib.util

class master():
    def __init__(self, sh):
        sh.log.info('init master')
        self.sh = sh
        self.sh.plugins = self
        self.plugins = {}
        if not 'plugins' in self.sh.cfg.data:
            self.sh.cfg.data['plugins'] = {}
            self.sh.cfg.save()

    def load(self, in_data):
        self.sh.log.info('load master')
        if isinstance(in_data, str):
            data = [in_data]
        elif isinstance(in_data, list):
            data = in_data
        for name in data:
            self._load(name)

    def _load(self, name):
        if name in self.plugins:
            return
        self.sh.log.info('load: ' + name)
        file = self.sh.const.path + '/plugins/' + name + '/__init__.py'
        if not os.path.exists(file):
            self.sh.log.error('plugin nicht gefunden: ' + name)
            return None
        spec = importlib.util.spec_from_file_location(name, file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not hasattr(mod, 'plugin'):
            self.sh.log.error('Klasse plugin nicht gefunden')
            return None
        plugin = mod.plugin(self.sh, name)
        if plugin.loaded:
            plugin.run()

    def stop(self):
        for plugin in self.plugins:
            self.plugins[plugin].stop()

class base():
    def __init__(self, sh, name):
        self.sh = sh
        self.name = name
        self.require = []
        self.cfg = {}
        self.lib = {}
        self.loaded = False

    def get_requirements(self):
        self.sh.log.info('get_requirements')
        self.sh.plugins.load(self.require)
        ok = True
        for plugin in self.require:
            if plugin in self.sh.plugins.plugins:
                self.lib[plugin] = self.sh.plugins.plugins[plugin]
            else:
                ok = False
        self.loaded = ok

    def run(self):
         pass

    def stop(self):
         pass
