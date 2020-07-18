import requests
import json

import plugins
import bin.sensor as sensor_base

import plugins.openweathermap.web as web
import plugins.openweathermap.sensor as sensor

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
        self.sh.log.info('run')
        try:
            sensor.load(self.sh)
        except Exception as e:
            self.sh.log.error(str(e))
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
                             sensor.new_value(element, data['current'][element], data['current']['dt'])
                    for element in data['current']['weather'][0]:
                        sensor.new_value('weather_'+element, data['current']['weather'][0][element], data['current']['dt'])
                    if 'rain' in data['current']:
                        for element in data['current']['rain']:
                            sensor.new_value('rain_'+element, data['current']['rain'][element], data['current']['dt'])
                    lenarr = len(data['daily'])
                    l = 0
                    while l < lenarr:
                        daily = data['daily'][l]
                        for element in daily:
                            if element != 'dt' and element != 'temp' and element != 'feels_like' and element != 'weather':
                                sensor.new_value('daily_' + str(l) + '_' + element, data['daily'][l][element], data['daily'][l]['dt'])
                        for element in data['daily'][l]['temp']:
                            sensor.new_value('daily_' + str(l) + '_temp_' + element, data['daily'][l]['temp'][element], data['daily'][l]['dt'])
                        for element in data['daily'][l]['feels_like']:
                            sensor.new_value('daily_' + str(l) + '_feels_like_' + element, data['daily'][l]['feels_like'][element], data['daily'][l]['dt'])
                        for element in data['daily'][l]['weather'][0]:
                            sensor.new_value('daily_' + str(l) + '_weather_' + element, data['daily'][l]['weather'][0][element], data['daily'][l]['dt'])
                        l += 1
            except Exeception as e:
                self.sh.log.error(str(e))
            print("Anzahl: ", len(self.sensors))

    def stop(self):
        if self.timer:
            self.timer.stop()
        sensor.save(self.sh)

    def _set_config(self, data):
        self.cfg['api'] = data['api']
        self.cfg['intervall'] = data['intervall']
        self.sh.cfg.data['plugins'][self.name]['api'] = data['api']
        self.sh.cfg.data['plugins'][self.name]['intervall'] = data['intervall']
        self.sh.cfg.save()

    def sm_backend(self, data):
        data = web.sm_backend(self.sh, self, data)
#cmd = data['cmd'].split('.')[2] return data['data'] if cmd == "get_config": return {'api': self.cfg['api'], 'intervall': self.cfg['intervall']} 
#        elif cmd == "set_config":
#           self._set_config(data) return {} else: print(cmd)
        return data
