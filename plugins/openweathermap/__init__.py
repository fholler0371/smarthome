import requests
import json

import plugins
import bin.sensor as sensor_base

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

        self.timer = None
        self.sensors = {}

    def run(self):
        self.timer = self.lib['timer'].start(self.cfg['intervall'], self.job)

    def job(self):
        if self.cfg['api'] != "" and hasattr(self.sh.const, 'geo'):
            url = "https://api.openweathermap.org/data/2.5/onecall?units=metric&lang=de&"
            url += 'lat='+str(self.sh.const.geo['lat'])+'&lon='+str(self.sh.const.geo['long'])+'&exclude=minutely,hourly&apikey='+self.cfg['api']
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    data = json.loads(r.content.decode())
                    for element in data['current']:
                        if element != 'dt' and element != 'weather' and element != 'rain':
                             if not (element in self.sensors):
                                 self.sensors[element] = sensor_base.sensor()
                             self.sensors[element].val(element, data['current'][element], data['current']['dt'])
                    for element in data['current']['weather'][0]:
                        name = 'weather_'+element
                        if not (name in self.sensors):
                            self.sensors[name] = sensor_base.sensor()
                        self.sensors[name].val(name, data['current']['weather'][0][element], data['current']['dt'])
                    if 'rain' in data['current']:
                        for element in data['current']['rain']:
                            name = 'rain_'+element
                            if not (name in self.sensors):
                                self.sensors[name] = sensor_base.sensor()
                            self.sensors[name].val(name, data['current']['rain'][element], data['current']['dt'])
                    lenarr = len(data['daily'])
                    l = 0
                    while l < lenarr:
                        daily = data['daily'][l]
                        for element in daily:
                            if element != 'dt' and element != 'temp' and element != 'feels_like' and element != 'weather':
                                name = 'daily_' + str(l) + '_' + element
                                if not (name in self.sensors):
                                    self.sensors[name] = sensor_base.sensor()
                                self.sensors[name].val(name, data['daily'][l][element], data['daily'][l]['dt'])
                        for element in data['daily'][l]['temp']:
                                name = 'daily_' + str(l) + '_temp_' + element
                                if not (name in self.sensors):
                                    self.sensors[name] = sensor_base.sensor()
                                self.sensors[name].val(name, data['daily'][l]['temp'][element], data['daily'][l]['dt'])
                        for element in data['daily'][l]['feels_like']:
                                name = 'daily_' + str(l) + '_feels_like_' + element
                                if not (name in self.sensors):
                                    self.sensors[name] = sensor_base.sensor()
                                self.sensors[name].val(name, data['daily'][l]['feels_like'][element], data['daily'][l]['dt'])
                        for element in data['daily'][l]['weather'][0]:
                                name = 'daily_' + str(l) + '_weather_' + element
                                if not (name in self.sensors):
                                    self.sensors[name] = sensor_base.sensor()
                                self.sensors[name].val(name, data['daily'][l]['weather'][0][element], data['daily'][l]['dt'])
                        l += 1
            except Exeception as e:
                self.sh.log.error(str(e))
            print(self.sensors)

    def stop(self):
        if self.timer:
            self.timer.stop()


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
