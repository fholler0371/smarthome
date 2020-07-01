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

import os
import sys
import time
import plugins
from threading import Thread
import subprocess

import psutil

import bin.ping as ping
import bin.config as config
import bin.log as log

class systemUpgradeThread(Thread):
    def __init__(self, log):
        Thread.__init__(self)
        self.log = log

    def run(self):
        self.log.info('System Update Start')
        responce = subprocess.Popen(('sudo apt-get update').split(' '), stdout=subprocess.PIPE).stdout.read()
        self.log.info('System Update Stop')
        self.log.info('System Upgrade Start')
        responce = subprocess.Popen(('sudo apt-get upgrade -y').split(' '), stdout=subprocess.PIPE).stdout.read()
        self.log.info('System Upgrade Stop')

class systemRebootThread(Thread):
    def __init__(self, log):
        Thread.__init__(self)
        self.log = log

    def run(self):
        self.log.info('System Reboot')
        responce = subprocess.Popen(('sudo reboot').split(' '), stdout=subprocess.PIPE).stdout.read()

class systemInstallThread(Thread):
    def __init__(self, log, sh):
        Thread.__init__(self)
        self.log = log
        self.sh = sh

    def run(self):
        self.log.info('System Install')
        name = self.sh.basepath + '/tmp/install_it.sh'
        f = open(name, 'w')
        f.write('wget -q -O - https://raw.githubusercontent.com/fholler0371/smarthome/master/install.sh | bash')
        f.close()
        response = subprocess.Popen(('bash ' + name).split(' '), stdout=subprocess.PIPE).stdout.read()
        out = response.decode(errors= 'backslashreplace')
        os.remove(name)

class plugin(plugins.base):
    ''' Klasse des Plugins mit den Standard Parametern '''
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')

        ''' Prüfen der Konfig und sezen ggf. der defaults'''
        val = {
            'port' : 4050,
            'path' : 'www/backend/client',
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

    def run(self):
        ''' starten des Plugins '''
        self.sh.log.info('run')
        if self.loaded:
            self.server = self.lib['webserver'].webserver_run(self.cfg['port'], self.cfg['path'], self.cfg['lib'], self.api)

    def stop(self):
        ''' stopen des des Plugins zum Ende des Programms '''
        if self.server:
            self.lib['webserver'].webserver_stop(self.server, self.cfg['port'])

    def _get_state(self):
        out = {}
        response = subprocess.Popen(('cat /sys/firmware/devicetree/base/model').split(' '), stdout=subprocess.PIPE).stdout.read()
        out['type'] = response.decode(errors= 'backslashreplace')
        response = subprocess.Popen(('cat /proc/meminfo').split(' '), stdout=subprocess.PIPE).stdout.read().decode().split('\n')
        value = response[0]
        while value.find('  ') > -1:
            value = value.replace('  ', ' ')
        value = int(value.split(' ')[1])/1024/1024
        value = ("{:.3f}".format(value)).replace('.', ',') + ' GiB'
        out['mem'] = value
        value = response[1]
        while value.find('  ') > -1:
            value = value.replace('  ', ' ')
        value = int(value.split(' ')[1])/1024/1024
        value = ("{:.3f}".format(value)).replace('.', ',') + ' GiB'
        out['free'] = value
        response = subprocess.Popen(('cat /sys/class/thermal/thermal_zone0/temp').split(' '), stdout=subprocess.PIPE).stdout.read()
        out['temp'] = ("{:.1f}".format(int(response.decode())/1000)).replace('.', ',')+' C'
        out['hostname'] = os.uname()[1]
        value = psutil.disk_usage(self.sh.const.path)
        out['disk'] = ("{:.2f}".format(value.free/1024/1024/1024)).replace('.', ',') + ' GiB '
        out['disk'] += ("{:.1f}".format(100-value.percent)).replace('.', ',') + '%'
        value = int(time.time() - psutil.boot_time())
        out['uptime'] = ('0'+str(value % 60))[-2:]
        value = int(value/60)
        out['uptime'] = ('0'+str(value % 60))[-2:] + ':' + out['uptime']
        value = int(value/60)
        out['uptime'] = ('0'+str(value % 24))[-2:] + ':' + out['uptime']
        value = int(value/24)
        if value > 0:
            out['uptime'] = str(value) + 'd ' + out['uptime']
        value = int(time.time() - self.sh.const.start_time)
        out['shtime'] = ('0'+str(value % 60))[-2:]
        value = int(value/60)
        out['shtime'] = ('0'+str(value % 60))[-2:] + ':' + out['shtime']
        value = int(value/60)
        out['shtime'] = ('0'+str(value % 24))[-2:] + ':' + out['shtime']
        value = int(value/24)
        if value > 0:
            out['shtime'] = str(value) + 'd ' + out['shtime']
        response = subprocess.Popen(('uname -r').split(' '), stdout=subprocess.PIPE).stdout.read()
        out['kernalversion'] = response.decode(errors= 'backslashreplace').split('\n')[0]
        response = subprocess.Popen(('cat /etc/os-release').split(' '), stdout=subprocess.PIPE).stdout.read()
        out['osname'] = response.decode(errors= 'backslashreplace').split('"')[1]
        out['python'] = sys.version.split(' ')[0]
        out['serial'] = self.sh.const.serial
        out['version'] = self.sh.const.version
        out['ip'] = self.sh.const.ip.split('/')[0]
        return out

    def _system_update(self):
        th = systemUpgradeThread(self.sh.log)
        th.start()

    def _system_reboot(self):
        th = systemRebootThread(self.sh.log)
        th.start()

    def _system_install(self):
        th = systemInstallThread(self.sh.log, self.sh)
        th.start()

    def _system_plugins(self):
        out = []
        for name in os.listdir(self.sh.const.path + '/plugins'):
           if not name.startswith('__'):
               cfg = config.load(self.sh, name + '/properties' , path='plugins')
               if cfg.data != {}:
                   out.append({'name': name, 'active': name in self.sh.plugins.plugins, 'background': cfg.data['background'],
                     'friendly': cfg.data['friendly'], 'description': cfg.data['description']})
        return out

    def _system_plugin_change(self, data):
        if data['value']:
            if ('__' + data['name'] + '__') in self.sh.cfg.data['plugins']:
                self.sh.cfg.data['plugins'][data['name']] = self.sh.cfg.data['plugins']['__' + data['name'] + '__']
                del self.sh.cfg.data['plugins']['__' + data['name'] + '__']
            else:
                self.sh.cfg.data['plugins'][data['name']] = {}
        else:
            self.sh.cfg.data['plugins']['__' + data['name'] + '__'] = self.sh.cfg.data['plugins'][data['name']]
            del self.sh.cfg.data['plugins'][data['name']]
        self.sh.cfg.save()

    def _system_plugin_logs(self):
        f = open(log.file_name, 'r+')
        lines = f.read().split('\n')
        f.close()
        lenarray = len(lines) - 2
        out = []
        while lenarray > -1:
            out.append(lines[lenarray])
            lenarray -= 1
        return '<br>'.join(out)

    def _get_plugins(self):
        out = {'plugins': [{'label':'System', 'name':'system'}]}
        for name in self.sh.plugins.plugins:
            cfg = config.load(self.sh, name + '/properties' , path='plugins')
            if 'backend_web' in cfg.data:
                out['plugins'].append({'label':cfg.data['friendly'], 'name':name})
        return out

    def _system_get_var(self):
        out = {'master': False, 'geo': {'lat': 52.5092947, 'long': 13.4178536}}
        if hasattr(self.sh.const, 'geo'):
            out['geo'] = self.sh.const.geo
        if hasattr(self.sh.const, 'master'):
            out['master'] = self.sh.const.master
        return out

    def _system_set_var(self, data):
        self.sh.const.geo = data['geo']
        self.sh.cfg.data['geo'] = data['geo']
        self.sh.const.master = data['master']
        self.sh.cfg.data['master'] = data['master']
        self.sh.cfg.save()

    def api(self, data_in):
        data = data_in['data']
        if data['cmd'] == 'get_hostname':
            return {'hostname': os.uname()[1]}
        elif data['cmd'] == 'client_get_plugins':
            return self._get_plugins()
        elif data['cmd'] == 'client_get_state':
            return self._get_state()
        elif data['cmd'] == 'client_system_update':
            self._system_update()
            return {}
        elif data['cmd'] == 'client_system_reboot':
            self._system_reboot()
            return {}
        elif data['cmd'] == 'client_system_install':
            self._system_install()
            return {}
        elif data['cmd'] == 'client_system_restart':
            self.sh.running = False
            return {}
        elif data['cmd'] == 'client_system_plugins':
            return self._system_plugins()
        elif data['cmd'] == 'client_system_plugin_change':
            self._system_plugin_change(data)
            return {}
        elif data['cmd'] == 'client_system_logs':
            return {'log': self._system_plugin_logs()}
        elif data['cmd'] == 'client_system_get_var':
            return self._system_get_var()
        elif data['cmd'] == 'client_system_set_var':
            return self._system_set_var(data)
        else:
            name = data['cmd'].split('.')[1]
            if name in self.sh.plugins.plugins:
                plugin = self.sh.plugins.plugins[name]
                return plugin.webserver_api(data)
        return data_in['data']
