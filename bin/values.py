# -*- coding: utf-8 -*-
"""Konstanten

    es werden Konstanten für den aktuellen Lauf des Programms ermittel und zur
    Verfügug gestellt. Die Werte werden im Verlauf des Programms nicht mehr 
    geändert.

Todo:
    - Plugins

Verlauf:
    2020-06-23 Basis erstellt
"""

import os
import time
import subprocess
import __main__

import psutil
import yaml

from bin import ping

class basic():
    ''' Klasse zum halten der Konstanten '''
    def __init__(self):
        ''' Ermittlung der Process-ID und ob das Programm als Service lauft.
        Wenn nicht wird eine andere Konfiguration geladen, z.B. als Testum-
        gebung
        '''
        self.pid = os.getpid()
        self.is_service = psutil.Process(self.pid).parent().pid < 5

        '''Ermitlung des Basispfades und des Namen des Programms '''
        file = os.path.abspath(__main__.__file__)
        self.path = os.path.dirname(file)
        self.name = os.path.splitext(os.path.basename(file))[0]

        ''' setzen der Startzeit '''
        self.start_time = time.time()

        self.serial = 'None'
        for entry in subprocess.Popen(('cat /proc/cpuinfo').split(' '), stdout=subprocess.PIPE).stdout.read().decode().split('\n'):
            if entry.startswith('Serial'):
                self.serial = entry.split(': ')[1]

        f = open(self.path+'/etc/version.yaml', 'r+')
        data = yaml.safe_load(f)
        f.close()
        self.version = data['version']

        self.ip = ping.guess_network()
        self.master = False

        self.server_name = os.uname()[1]
        self.friendly_name = os.uname()[1]

        self.aes_key = ''
