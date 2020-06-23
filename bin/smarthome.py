# -*- coding: utf-8 -*-
"""Hauptmodul mit der Klasse smarthome

Todo:
    - Plugins

Verlauf:
    2020-06-21 Core erstellt
"""

import os
import sys
import time
import threading
import subprocess
import signal
import __main__

import psutil

import bin.log as logging
import bin.config_json as config_json
import bin.module as modul_loader
import bin.timer as timer

''' SH globale Variable der Smarthomeklasse '''
SH = None

def handler(signum, frame):
''' Handler fuer Signal events kill und KeyboardInterrupt '''
    global SH
    SH.running = False
    print('Signal handler called with signal', signum)

class smarthome:
    def __init__(self):
        ''' Initialiesierung der Klasse
        
        Returns:
            Klasse
        '''

        ''' Setzen der Globalen Variable '''
        global SH
        SH = self

        ''' Setzen der Hauptvariablen '''
        self.running = True
        self.pid = os.getpid()
        file = os.path.abspath(__main__.__file__)
        self.basepath = os.path.dirname(file)
        self.basename = os.path.splitext(os.path.basename(file))[0]
        self.is_service = self.__is_service()

        ''' setzen der Hooks fuer Kill und KeyboardInterrupt '''
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)
        
        ''' wurde das Programm mit Parametern gestartet ?'''
        if len(sys.argv) > 1:
            import bin.cmd_line_tools as tools
            tools.run(self)
            sys.exit()

        ''' Intialiesierung des Loggers '''
        self.log = logging.getLogger(self.basename)

        ''' Laden der Konfiguration '''
        cfg_file = self.basename
        if not self.is_service: #Nutzen einer config fuer den Start von Console
            cfg_file += '.cmd'
        self.cfg = config_json.load(self, cfg_file)
        
        ''' Anpassen des Loggers an Konfiguration '''
        if 'logger' in self.cfg.data:
            logging.update(self, self.log, self.cfg.data['logger'])
        else:
            self.log.error("kein Eintrag fuer logger in der konfiguration")
            
        ''' Laden und Starten des internen Timer-Moduls '''
        self.timer = timer.get(self)
        
        ''' Laden der Module '''
        self.module = []
        modul_loader.scan(self) #suchen nach neuen Modulen
        if 'module' in self.cfg.data:
            for modul in  self.cfg.data['module']:
                if self.cfg.data['module'][modul]['active']:
                    mod = modul_loader.load(self, modul)
                    if mod != None:
                        self.module.append(mod)
                        mod.start()

    def run(self):
        ''' Starten der Haupt Funktion
        self.log.info("run")
        '''
        
        ''' Setzen des Konsolen Timeouts '''
        timeout = 30 # default fuer Timeout der Konsole
        if 'timeout' in self.cfg.data:
            timeout = self.cfg.data['timeout']
        timeout += time.time()
        
        ''' Hauptschleife '''
        while self.running and (self.is_service or timeout > time.time()):
            time.sleep(1)
            
        ''' Stoppen der Module '''    
        for mod in self.module:
            mod.stop()
            
        ''' Stoppen des Timers '''
        if not self.timer == None:
            self.timer.stop()
            
        ''' Warten auf das Ende aller Threads '''    
        for th in threading.enumerate():
            if not th == threading.main_thread():
                th.join()
                
        self.log.info("run beendet")

    def __is_service(self):
        self.log.info("Check Service")
        ''' Check ob das Programm als Service lauft

        Returns:
            True wenn Service
        '''
        return psutil.Process(self.pid).parent().pid < 5
