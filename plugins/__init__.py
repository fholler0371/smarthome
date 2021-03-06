# -*- coding: utf-8 -*-
"""Plugins

    Es werden Konfigurationen geladen ggf. auch ein .default File.
    aktuell werden nur json Dateien unterstützt

Todo:
    - scan der Verfügbaren Klassen

Verlauf:
    2020-06-25 Funktion in Konfugaration verschoben
    2020-06-23 Basis erstellt
"""

import os
import importlib.util

import bin.config as config

class master():
    ''' Masterklasse zum verwalten der Plugins '''
    def __init__(self, sh):
        ''' Initialiesierung der Variabelen

        Param:
            sh: Referenze zum Smarthome-System'''
        sh.log.info('init master')
        self.sh = sh
        self.sh.plugins = self
        self.plugins = {}

        ''' Erstellung einer Sektion Plugins in der Konfiguration, wenn noch
        nicht vorhanden '''
        if not ('plugins' in self.sh.cfg.data):
            self.sh.cfg.data['plugins'] = {}
            self.sh.cfg.save()

    def load(self, in_data):
        ''' Laden von Plugins

        Param:
            in_data: - kann ein Name str sein
                     - ein Array mit Namen
        '''
        self.sh.log.info('load master')

        ''' Umformen des Inputs zum Array '''
        if isinstance(in_data, str):
            data = [in_data]
        elif isinstance(in_data, list):
            data = in_data
        elif isinstance(in_data, dict):
            data = []
            for name in in_data:
                if not(name.startswith('__')):
                    data.append(name)

        ''' serielles laden '''
        for name in data:
            self._load(name)

    def _load(self, name):
        ''' Laden eines Plugins

        Param:
            name: des Plugins
        '''

        ''' Stop, wenn Plugin schon geladen '''
        if name in self.plugins:
            return

        self.sh.log.info('load: ' + name)

        ''' Kompletten Pfad erstellen und auf existens pruefen'''
        file = self.sh.const.path + '/plugins/' + name + '/__init__.py'
        if not os.path.exists(file):
            self.sh.log.error('plugin nicht gefunden: ' + name)
            return None

        ''' Laden des Plugins '''
        spec = importlib.util.spec_from_file_location(name, file)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            self.sh.log.error(str(e))
        if not hasattr(mod, 'plugin'):
            self.sh.log.error('Klasse plugin nicht gefunden')
            return None
        try:
            plugin = mod.plugin(self.sh, name)
        except Exception as e:
            self.sh.log.error(str(e))

        ''' wenn alles gut gelaufen ist starten des Plugins '''
        self.sh.log.info("plugin load " + name + " " + str(plugin.loaded))
        if plugin.loaded:
            plugin.run()

    def stop(self):
        self.sh.log.info('stop')
        ''' stoppen aller Plugins, zum Programmende'''
        for plugin in self.plugins:
            self.plugins[plugin].stop()

    def register(self, plugin):
        ''' registrieren von Plugins

        Param:
            plugin: das Plugin das registriert werden soll
        '''
        self.sh.log.info('rgisterer')

        self.plugins[plugin.name] = plugin

class base():
    ''' Basis Klasse mit allgemeinen Funktionen'''
    def __init__(self, sh, name):
        ''' Intialiesieren der Variablen

        Param:
            sh: SmartHome Object
            name: Name des Plugins
        '''
        self.sh = sh
        self.name = name
        self.friendly_name = name
        self.require = []
        self.cfg = {}
        self.lib = {}
        self.loaded = False

    def get_requirements(self):
        ''' Aufloesen der Abhaegigkeiten'''
        self.sh.log.info('get_requirements')

        ''' Laden der notwendigen Plugins '''
        self.sh.plugins.load(self.require)

        ''' Pruefen ob alle Plugins geladen wurden'''
        ok = True
        for plugin in self.require:
            if plugin in self.sh.plugins.plugins:
                self.lib[plugin] = self.sh.plugins.plugins[plugin]
            else:
                ok = False
        self.loaded = ok

    def create_config(self, defaults):
        self.sh.log.info('crete_config')
        self.sh.log.debug(str(defaults))
        ''' pruefe Konfiguration und setze ggf. defaults

        Param:
            default: Standardkonfiguration
        '''
        change = False

        ''' ist eine Kpnfuguration vorhanden '''
        if not (self.name in self.sh.cfg.data['plugins']):
            self.sh.cfg.data['plugins'][self.name] = {}
            change = True

        ''' setze ggf. Standard '''
        val = self.sh.cfg.data['plugins'][self.name]
        defaults.update(val)
        self.sh.cfg.data['plugins'][self.name] = defaults
        if defaults != val:
            change = True

        ''' Wenn notwendig speichern der Konfuguration '''
        if change:
            self.sh.cfg.save()

        ''' setze Konfig '''
        self.cfg = defaults

        if not('friendly_name' in self.cfg):
            cfg = config.load(self.sh, self.name + '/properties' , path='plugins')
            if 'friendly' in cfg.data:
                self.cfg['friendly_name'] = cfg.data['friendly']
            else:
                self.cfg['friendly_name'] = self.name
            self.sh.cfg.data['plugins'][self.name]['friendly_name'] = self.cfg['friendly_name']
            self.sh.cfg.save()
        self.sh.log.info('crete_config finish')

    def run(self):
        ''' Dummy Run '''
        pass

    def stop(self):
        ''' Dummy Pass'''
        pass

    def webserver_api(self, data):
        return data
