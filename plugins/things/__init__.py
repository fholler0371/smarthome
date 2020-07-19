from threading import Thread, Timer

import plugins

import plugins.things.sensor as sensor
import plugins.things.web as web

class plugin(plugins.base):
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')
        val = {}
        self.create_config(val)
        self.loaded = True
        if self.loaded:
            self.sh.plugins.register(self)

    def run(self):
        sensor.load(self.sh, self)

    def new_sensor_value(self, data):
        sensor.new_value(data)

    def sm_backend(self, data):
        data = web.sm_backend(self.sh, self, data)
        return data
