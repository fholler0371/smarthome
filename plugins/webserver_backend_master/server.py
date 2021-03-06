# -*- coding: utf-8 -*-
"""Webserver

   Basisklasse fuer alle Webzugaenge

Todo:
    - Post call zur API
    - Umarbeiten des Mimecodes

Verlauf:
    2020-06-25 Last Call
    2020-06-24 Basis erstellt
"""

import os
import json
import threading
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from functools import partial
import urllib.request

class last_call(Thread):
    ''' Classe zum senden des Last-Call '''
    def __init(self, url):
        ''' Init Funktion
        Param:
            url: Link der versucht wird
        '''
        Thread.__init__(srelf)
        self.url = url

    def run(self):
        urllib.request.urlopen(self.url)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        """Handle requests in a separate thread."""

class webserverHandler(BaseHTTPRequestHandler):
    ''' Handler fuer Anfragen von den Browsern '''
    def __init__(self, sh, path, lib, api, capi, *args, **kwargs):
        ''' Initialiesierung der Klasse
        Param:
            sh: smarthome Object
            path: Pfad der statischen Projekt-dateien
            lib: Pfad der statischen Dateien die fuer alle Server gelten
            api: Call zur API durch post requests
        '''
        self.sh = sh
        self.root_path = path
        self.root_lib = lib
        self.api = api
        self.capi = capi
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        ''' sendet die logs an den Standard logger '''
        self.sh.log.info("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(),format%args))

    def do_POST(self):
        self.sh.log.info('call from '+self.client_address[0])
#        print(self.path)
#        print(self.client_address)
#        print(self.headers)
        content_len = int(self.headers['Content-Length'])
        if '/api' == self.path:
            ret = self.api({'data':json.loads(self.rfile.read(content_len).decode())})
        elif '/client-api' == self.path:
            ret = self.capi({'source-ip': self.client_address[0],
                             'headers': str(self.headers).split('\n'),
                             'data':json.loads(self.rfile.read(content_len).decode())})
        else:
            ret = {}
        data = json.dumps(ret).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        size = len(data)
        self.send_header('Content-Length', str(size))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        ''' Bearbeitung von get requests d.h. statischen Anfragen '''
        path = self.path

        ''' Anfuegen von index.html, wenn Anfrage nur an Folder geht '''
        if path.endswith('/'):
            path += 'index.html'

        ''' setzen des Root-Pfades in Abhängigkeit ob Libary oder Plugin
        spezifischer Pfad ''' 
        if path.startswith('/lib/'):
            path = self.sh.const.path + '/' + self.root_lib + '/' + path[5:]
        else:
            path = self.sh.const.path + '/' + self.root_path + '/' + path[1:]

        ''' Blockieren des Hochwanderns in der Verzeichnisstruktur'''
        path = path.replace('/./', '/').replace('/../', '/').replace('//', '/').replace('/.', '/')

        ''' senden der Dateien '''
        if not os.path.exists(path):
            self.send_response(404)
            self.send_header('Content-Type',
                             'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('error 404'.encode('utf-8'))
            return
        self.send_response(200)
        known = True
        if path.endswith('.html'):
            self.send_header('Content-Type', 'text/html; charset=utf-8')
        elif path.endswith('.js'):
            self.send_header('Content-Type', 'application/javascript')
        elif path.endswith('.css'):
            self.send_header('Content-Type', 'text/css')
        elif path.endswith('.png'):
            self.send_header('Content-Type', 'image/png')
        else:
            known = False
        if known:
            size = os.path.getsize(path)
            self.send_header('Content-Length', str(size))
            self.end_headers()
            file = open(path, 'rb')
            self.wfile.write(file.read())
            file.close()
        else:
            self.send_header('Content-Type',
                             'text/txt; charset=utf-8')
            self.end_headers()
            self.wfile.write('unbekannter typ'.encode('utf-8'))

class loopThread(Thread):
    ''' class fuer den dauer Loop des Servers '''
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        self.server.serve_forever()

class server:
    def __init__(self, sh):
        ''' Standard init des Plugins '''
        self.sh = sh
        self.sh.log.info('__init__')

    def webserver_run(self, port, path, lib, api, capi):
        ''' Startet einen Webserver

        Param:
            port: Port an dem der Server hoeren soll
            path: Pfad der statischen Dateien
            lib: Pfad der Standard-Bibliotheken
            api: Funktion fuer Post calls

        Return:
            Object des HTTPServer
        '''
        self.sh.log.info('webserver_run')
        self.port = port

        ''' Erstellen des Servers '''
        handler = partial(webserverHandler, self.sh, path, lib, api, capi)
        self.server = ThreadedHTTPServer(('0.0.0.0', port), handler)

        ''' Starten des Servers '''
        th = loopThread(self.server)
        th.start()


    def webserver_stop(self):
        ''' Stopt den Webserver und sendet Last-Call
        Param:
            server: server objeckt
            port: port des servers
        '''
        self.sh.log.info('webserver_stop')

        if self.server:
            self.server.shutdown()

        ''' sende Last-Call '''
        try:
            last_call("http://localhost:"+str(self.port)).start()
        except:
            pass
