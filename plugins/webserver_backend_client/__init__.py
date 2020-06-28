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
import time
import plugins
from threading import Thread
import subprocess

import psutil

import bin.ping as ping

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
        out['ip'] = ping.guess_network().split('/')[0]
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

    def api(self, data_in):
        data = data_in['data']
        if data['cmd'] == 'get_hostname':
            return {'hostname': os.uname()[1]}
        elif data['cmd'] == 'client_get_plugins':
            return {'plugins': [{'label':'System', 'name':'system'}]}
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
        return data_in['data']

