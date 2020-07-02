import requests
import json

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

        self.timer = None

    def run(self):
        self.timer = self.lib['timer'].start(self.cfg['intervall'], self.job)

    def job(self):
        if self.cfg['api'] != "" and hasattr(self.sh.const, 'geo'):
            url = "https://api.openweathermap.org/data/2.5/onecall?units=metric&lang=de&"
            url += 'lat='+str(self.sh.const.geo['lat'])+'&lon='+str(self.sh.const.geo['long'])+'&exclude=minutely&apikey='+self.cfg['api']
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    data = json.loads(r.content.decode())
                    for element in data['current']:
                        if element != 'dt' and element != 'weather' and element != 'rain':
                             print(data['current']['dt'], element, data['current'][element])
                    for element in data['current']['weather'][0]:
                        print(data['current']['dt'], 'weather_'+element, data['current']['weather'][0][element])
                    for element in data['current']['rain']:
                        print(data['current']['dt'], 'rain_'+element, data['current']['weather'][element])
                    lenarr = len(data['daily'])
                    for daily in data['daily']:
                        for element in daily:
                            print(element)
            except Exeception as e:
                self.sh.log.error(str(e))
                print(str(e))

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
