import os

import importlib.util

class master():
    def __init__(self, sh):
        sh.log.info('init master')
        self.sh = sh
        self.sh.plugins = self
        self.plugins = []

    def load(self, in_data):
        self.sh.log.info('load master')
        if isinstance(in_data, str):
            data = [in_data]
        for name in data:
            self._load(name)

    def _load(self, name):
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
        cls = mod.plugin(self.sh, name)


class base():
    def __init__(self, sh, name):
        self.sh = sh
        self.name = name
        self.requirements = []
