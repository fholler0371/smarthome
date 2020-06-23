#!/media/pi/data/SM/smarthome/env/bin/python3

# -*- coding: utf-8 -*-
"""SmartHome Start Script

Dieses Script ist zum Starten des SmartHome Programms

Es sind folgende Parameter möglich:
    install
        Installiert das Script als Dienst
    uninstall
        Deinstalliert den Dient
    start
        Starte den Dienst
    stop
        Stopt den Dient
    restart
        Führt nach einander Start stop und start aus
    status
        gibt Informationen über den Dienst aus
   
Der Pfad zum Interpreter in der ersten Zeile wir durch das Installscript
auf den passenden Interpreter im virtuellen Enviroment angepasst.

Todo:

Version:
"""

from bin.smarthome import smarthome as sh

smarthome = sh()
''' Lädt das Hauptmodul vom Smarthome '''

smarthome.run()
''' Startet die das Modul '''
