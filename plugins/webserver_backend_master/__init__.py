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
import plugins.webserver_backend_master.auth as auth

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
        self.require = ['webserver', 'net_broadcast']
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
        hosts = self.lib['net_broadcast'].scan()
        return hosts
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

    def getClientAPI(self, data):
        jdata = json.dumps(data).encode()
        out = {}
        with urllib.request.urlopen('http://' + data['client'] + ':' + str(self.cfg['client_port']) + '/api', jdata) as f:
            out = json.loads(f.read().decode())
        return out

    def api(self, data_in):
        data = data_in['data']
        print(data)
        if 'client' in data:
            if 'master' == data['client']:
                if 'get_salt' == data['cmd']:
                    out = auth.getSalt(self.sh, data)
                elif 'keep_alive' == data['cmd']:
                    out = auth.decode(self.sh, data)
                    if out['login']:
                        out = auth.encode(self.sh, out)
                elif 'get_menu' == data['cmd']:
                    out = auth.decode(self.sh, data)
                    out['data'] = []
                    out['data'].append({'label': 'Smarthome - Backend Scan', 'mod': 'sm_backend', 'p1':'scan'})
                    if out['login']:
                        out = auth.encode(self.sh, out)
                elif 'get_server' == data['cmd']:
                    return {'name': self.sh.const.server_name, 'friendly_name': self.sh.const.friendly_name, 'master': self.sh.const.master}
                elif 'get_clients' == data['cmd']:
                    return  self.cfg['hosts']
                elif 'server_scan' == data['cmd']:
                    return self._scan_hosts()
                if not out['login']:
                    if 'token' in out:
                        del out['token']
                    del out['cmd']
                    del out['client']
                return out
        elif data['cmd'] == 'get_scan_state':
            return {'scan_state': self.scanning}
        elif data['cmd'] == 'get_remote_hosts':
            return {'hosts': self.cfg['hosts']}
        elif data['cmd'].startswith('client'):
            return self.getClientAPI(data)
        return data_in['data']
