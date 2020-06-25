# -*- coding: utf-8 -*-
"""Plugins

    Das Plugin stellt den Hauptzugriff für das Smarthome 
    Backend, es sollte daher auf dem Gateway laufen

    Der spezifische Webcode liegt in www/backend/master

Todo:
    - api fehlt noch
    - scan und speichern der Clients
    - auswahl des Clients
    - create Config in das Pluginbase verschieben #8
    - registrieren ins Base #7

Verlauf:
    2020-06-25 class LastCall entfernt
    2020-06-24 Basis erstellt
"""

import plugins

class plugin(plugins.base):
    ''' Klasse des Plugins mit den Standard Parametern '''
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')

        ''' Prüfen der Konfig und sezen ggf. der defaults '''
        self._create_config()

        ''' setzten und pruefen der Abhaengigkeiten '''
        self.require = ['webserver']
        self.get_requirements()

        ''' wenn alles Ok Plugin registrieren '''
        if self.loaded:
            self.sh.plugins.register(self)

        ''' setzen der defaults '''
        self.server = None

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
            self.server = self.lib['webserver'].webserver_run(self.cfg['port'], self.cfg['path'], self.cfg['lib'])

    def stop(self):
        ''' stopen des des Plugins zum Ende des Programms '''
        if self.server:
            self.lib['webserver'].webserver_stop(self.server, self.cfg['port'])
