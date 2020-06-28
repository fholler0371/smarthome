# -*- coding: utf-8 -*-
"""Verwalten von Konfigurationen

    Es werden Konfigurationen geladen ggf. auch ein .default File.
    aktuell werden nur json Dateien unterstützt

Todo:
    - yaml dateien

Verlauf:
    2020-06-23 Basis erstellt
"""

import os
import json

import yaml

class cfg:
    ''' Klasse zum laden der Konfigurationen '''
    def __init__(self, sh, file, format= 'yaml'):
        ''' Init Proezdur

        Param:
            sh: referenz zum SmartHome Objekt
            file: der Dateiname
            format: >> aktuell nicht unterstützt
        '''

        ''' Da beim Start das Logging noch nicht verfügbar ist, wird die Log-
        Klasse in der Datei abgeprueft
        '''
        if hasattr(sh, 'log'):
            sh.log.info('__init__')

        self.sh = sh
        self.data = {}
        self.format = format

        ''' Erstellen des vollständigen Namen des Files '''
        self.name = sh.const.path + '/etc/' + file
        if format == 'json':
            self.name += '.json'
        else:
            self.name += '.yaml'
        file_name = self.name

        ''' gegebenfalls versuch mit default '''
        if not os.path.exists(file_name):
            file_name += '.default'

        ''' Laden der Datei '''
        try:
            if format == 'json':
                f = open(file_name, 'r+')
                self.data = json.loads(f.read())
                f.close()
            else:
                f = open(file_name, 'r+')
                self.data = yaml.safe_load(f)
                f.close()

        except Exception as e:
            if hasattr(sh, 'log'):
                sh.log.error(str(e))

        ''' wenn in der Datei Objekt mit dem Namen nice, "schoenees" Speichern
        der Datei'''
        if 'nice' in self.data:
             del self.data['nice']
             self.save()

    def save(self):
        ''' Speichern der Datei, in einer gut lesbaren Variante '''
        if hasattr(self.sh, 'log'):
            self.sh.log.info('save')
        if self.format == 'json':
            f = open(self.name, 'w')
            f.write(json.dumps(self.data, indent=2, sort_keys=True))
            f.close()
        else:
            f = open(self.name, 'w')
            yaml.dump(self.data, f, default_flow_style=False)
            f.close()

def load(sh, file, format= 'yaml'):
    ''' Kurz form zum erstellen der Klasse, Parameter werden direkt ueber-
    gebeben

    Return:
        Klasse mit Konfiguration
    '''
    if hasattr(sh, 'log'):
        sh.log.info('load: '+file)

    return cfg(sh, file, format)
