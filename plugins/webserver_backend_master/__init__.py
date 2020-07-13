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
import bin.config as config
import plugins.webserver_backend_master.auth as auth
import plugins.webserver_backend_master.server as server
import plugins.webserver_backend_master.system as system

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
        self.require = ['net_broadcast']
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
        self.main_server = server.server(self.sh)
        self.main_server.webserver_run(self.cfg['port'], self.cfg['path'], self.cfg['lib'], self.api, self.client_api)

    def stop(self):
        ''' stopen des des Plugins zum Ende des Programms '''
        if self.main_server:
            self.main_server.webserver_stop()

    def _scan_hosts(self):
        hosts = self.lib['net_broadcast'].scan()
        data = json.dumps({'client': 'master', 'cmd':'get'}).encode()
        server = []
        for host in hosts:
            try:
                with urllib.request.urlopen('http://' + host['ip'] + ':' + str(self.cfg['port']) + '/api', data) as f:
                     server.append(host)
            except:
                pass
        self.cfg['hosts'] = server
        self.sh.cfg.data['hosts'] = server
        self.sh.cfg.save()

    def api(self, data_in):
        data = data_in['data']
        if 'client' in data:
            if 'master' == data['client']:
                if 'get_salt' == data['cmd']:
                    out = auth.getSalt(self.sh, data)
                elif 'get' == data['cmd']:
                    out = {'login': False}
                elif 'keep_alive' == data['cmd']:
                    out = auth.decode(self.sh, data)
                    if out['login']:
                        out = auth.encode(self.sh, out)
                elif 'get_menu' == data['cmd']:
                    out = auth.decode(self.sh, data)
                    out['data'] = []
                    if out['login']:
                        if 'sm_backend' in out['token']['packages']:
                            if self.sh.const.master:
                                if len(self.cfg['hosts']) > 0:
                                    inner = []
                                    for host in self.cfg['hosts']:
                                        inner.append({'label': host['friendly_name'], 'mod': 'sm_backend', 'p1':'client', 'p2':host['ip'],
                                                                                                           'p3': host['friendly_name']})
                                    out['data'].append({'label': 'Backends', 'sub': inner})
                                out['data'].append({'label': 'Smarthome - Backend Scan', 'mod': 'sm_backend', 'p1':'scan', 'display':False})
                            else:
                                out['data'].append({'label': 'Backend', 'mod': 'sm_backend', 'p1':'client', 'p2':self.sh.const.ip.split('/')[0],
                                                                                                            'p3':self.sh.const.friendly_name})
                        out = auth.encode(self.sh, out)
                elif 'get_server' == data['cmd']:
                    return {'name': self.sh.const.server_name, 'friendly_name': self.sh.const.friendly_name, 'master': self.sh.const.master}
                elif 'get_clients' == data['cmd']:
                    return  self.cfg['hosts']
            else:
                out = auth.decode(self.sh, data)
                if out['login']:
                    if 'sm_backend' == data['client'] and 'sm_backend' in out['token']['packages']:
                        if 'scan' == data['cmd']:
                            self._scan_hosts()
                        else:
                            if 'ip' in data['data']:
                                jdata = json.dumps(out).encode()
                                with urllib.request.urlopen('http://' + data['data']['ip'] + ':' + str(self.cfg['port']) + '/client-api', jdata) as f:
                                    out['data'] = json.loads(f.read().decode())
                    out = auth.encode(self.sh, out)
            if not out['login']:
                if 'token' in out:
                    del out['token']
            if 'cmd' in out:
                del out['cmd']
            if 'client' in out:
                del out['client']
            return out
        else:
            print('>>>> ERROR')
            print(data_in)
            return {}
        return data_in['data']

    def client_api(self, data):
        out = data['data']
        has_X_Real_IP = False
        for line in data['headers']:
            if line.startswith('X-Real-IP'):
                has_X_Real_IP = True
        if not(has_X_Real_IP) and ping.is_ip_in_range(self.sh.const.ip, data['source-ip']):
            if 'get_plugins' in data['data']['cmd']:
                out['data'] = {'plugins': [{'label':'System', 'name':'system'}]}
                for name in self.sh.plugins.plugins:
                    cfg = config.load(self.sh, name + '/properties' , path='plugins')
                    if 'backend_web' in cfg.data:
                        out['data']['plugins'].append({'label':cfg.data['friendly'], 'name':name})
            elif 'system' in data['data']['cmd']:
                out['data'] = system.call(self.sh, out)
            else:
                if data['data']['cmd'] in self.sh.plugins.plugins:
                    if hasattr(self.sh.plugins.plugins[data['data']['cmd']], 'sm_backend'):
                        out['data'] = self.sh.plugins.plugins[data['data']['cmd']].sm_backend(out)
                    else:
                        print('missing function')
                else:
                    print('plugin not found')
        return out['data']
