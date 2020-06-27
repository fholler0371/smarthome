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

from threading import Thread
import json
import urllib.request

import plugins
import bin.ping as ping

class scanThread(Thread):
    def __init__(self, log, net, pl, client_port):
        Thread.__init__(self)
        self.net = net
        self.pl = pl
        self.log = log
        self.client_port = client_port

    def run(self):
        ping_hosts = ping.scan(self.log, self.net)
        data = json.dumps({'cmd':'get_hostname'}).encode()
        hosts = []
        for host in ping_hosts:
            try:
                with urllib.request.urlopen('http://' + host + ':' + str(self.client_port) + '/api', data) as f:
                    hosts.append({'ip': host, 'hostname': json.loads(f.read().decode())['hostname']})
            except:
                pass
        self.pl.cfg['hosts'] = hosts
        self.pl.sh.cfg.data['plugins'][self.pl.name]['hosts'] = hosts
        self.pl.sh.cfg.save()
        self.pl.scanning = False

class plugin(plugins.base):
    ''' Klasse des Plugins mit den Standard Parametern '''
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')

        ''' Prüfen der Konfig und sezen ggf. der defaults'''
        val = {
            'port' : 4000,
            'client_port' : 4050,
            'path' : 'www/backend/master',
            'lib' : 'www/lib',
            'hosts': []
          }
        if not self.sh.const.is_service:
            val['port'] = val['port'] + 100
            val['client_port'] = val['client_port'] + 100
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
            th = scanThread(self.sh.log, self.cfg['network'], self, self.cfg['client_port'])
            th.start()
            self.scanning = True

    def api(self, data_in):
        data = data_in['data']
        if data['cmd'] == 'scan_clients':
            self._scan_hosts()
            return {'scan_state': self.scanning}
        elif data['cmd'] == 'get_scan_state':
            return {'scan_state': self.scanning}
        elif data['cmd'] == 'get_remote_hosts':
            return {'hosts': self.cfg['hosts']}
        return data_in['data']
