# -*- coding: utf-8 -*-
"""Plugins

    Das Plugin stellt den Hauptzugriff für das Smarthome 
    Backend, es sollte daher auf dem Gateway laufen

    Der spezifische Webcode liegt in www/backend/master

Todo:
    - api fehlt noch
    - scan und speichern der Clients
    - auswahl des Clients
    - close webserver nach webserver verscieben #6
    - registrieren ins Base #7

Verlauf:
    2020-06-25 Konfiguration in den Base verschieben
    2020-06-24 Basis erstellt
"""

import plugins
from threading import Thread

import bin.ping as ping

class scanThread(Thread):
    def __init__(self, log, net, pl):
        Thread.__init__(self)
        self.net = net
        self.pl = pl
        self.log = log

    def run(self):
        ping_hosts = ping.scan(self.log, self.net)
        for host in ping_hosts:
            print(host)

class plugin(plugins.base):
    ''' Klasse des Plugins mit den Standard Parametern '''
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')

        ''' Prüfen der Konfig und sezen ggf. der defaults'''
        val = {
            'port' : 4000,
            'path' : 'www/backend/master',
            'lib' : 'www/lib'
          }
        if not self.sh.const.is_service:
            val['port'] = val['port'] + 100
        self.create_config(val)

        ''' setzten und pruefen der Abhaengigkeiten '''
        self.require = ['webserver']
        self.get_requirements()

        ''' wenn alles Ok Plugin registrieren '''
        if self.loaded:
            self.sh.plugins.register(self)

        ''' setzen der defaults '''
        self.server = None
        self.scanning = False

    def _create_config(self):
        self.sh.log.info('_create_config')
        change = False
        if not self.name in self.sh.cfg.data['plugins']:
            self.sh.cfg.data['plugins'][self.name] = {}
            change = True
        if not 'port' in self.sh.cfg.data['plugins'][self.name]:
            self.sh.cfg.data['plugins'][self.name]['port'] = 4000
            if not self.sh.const.is_service:
                self.sh.cfg.data['plugins'][self.name]['port'] += 100
            change = True
        if not 'path' in self.sh.cfg.data['plugins'][self.name]:
            if not self.sh.const.is_service:
                self.sh.cfg.data['plugins'][self.name]['path'] = 'www/backend/master'
            change = True
        if not 'lib' in self.sh.cfg.data['plugins'][self.name]:
            if not self.sh.const.is_service:
                self.sh.cfg.data['plugins'][self.name]['lib'] = 'www/lib'
            change = True
        if change:
             self.sh.cfg.save()
        self.cfg = self.sh.cfg.data['plugins'][self.name]

    def run(self):
        ''' starten des Plugins '''
        self.sh.log.info('run')
        if self.loaded:
            self.server = self.lib['webserver'].webserver_run(self.cfg['port'], self.cfg['path'], self.cfg['lib'], self.api)

    def stop(self):
        ''' stopen des des Plugins zum Ende des Programms '''
        if self.server:
            self.lib['webserver'].webserver_stop(self.server, self.cfg['port'])

    def _scan_hosts(self):
        if not('network' in self.cfg):
            net = ping.guess_network()
            if net != '':
                self.cfg['network'] = net
                self.sh.cfg.data['plugins'][self.name]['network'] = net
                self.sh.cfg.save()
        if 'network' in self.cfg:
            th = scanThread(self.sh.log, self.cfg['network'], self)
            th.start()
            print('start scanning')
            print(self.cfg)
            self.scanning = True

    def api(self, data_in):
        data = data_in['data']
        if data['cmd'] == 'scan_clients':
            self._scan_hosts()
        return data_in['data']
