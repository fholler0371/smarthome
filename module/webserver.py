import time
import json
from module import modul_base as base
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
from threading import Thread

class backThread(Thread):
    def __init__(cls, server):
        Thread.__init__(cls)
        cls.server = server

    def run(cls):
        cls.server.serve_forever()

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        message = threading.currentThread().getName()
        self.wfile.write(message.encode('utf-8'))
        self.wfile.write(b'\n')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class modul(base):
    def __init__(cls, sh, cfg):
        base.__init__(cls, sh, cfg)
        cls.sh.log.info('__init__')
        cls.name = "WebServer"
        cls.has_menu = True
        cls.backend_server = None

    def start(cls):
        cls.sh.log.info('start')
        if not cls.running:
            cls.running = True
            if 'backend' in cls.cfg and cls.cfg['backend']:
                cls.backend_server = ThreadedHTTPServer(('0.0.0.0', cls.cfg['backend-port']), Handler)
                th = backThread(cls.backend_server)
                th.start()

    def stop(cls):
        cls.sh.log.info('stop')
        cls.running = False
        if cls.backend_server != None:
            cls.backend_server.shutdown()

    def menu_cli(cls, menu):
        cls.sh.log.info('menu_cli')
        cls.sh.log.debug(menu)
        out = '-'
        menu_levels = menu[5:].split('.')
        if len(menu_levels) == 1:
            out = json.dumps({'label': 'Bitte Modul aussuchen', 'entries' : [
                {'label' : 'Status', 'cmd': 'CMD ' + str(menu_levels[0]) + '.1'},
                {'label' : 'Backend aktivieren/deaktivieren', 'cmd': 'CMD ' + str(menu_levels[0]) + '.2'},
                ], 'exit':None})
        return out

    def cmd_cli(cls, cmd):
        cls.sh.log.info('cmd_cli')
        cls.sh.log.debug(cmd)
        out = '-'
        cmd_levels = cmd[4:].split('.')
        if len(cmd_levels) == 1:
            return out
        elif len(cmd_levels) == 2:
            if cmd_levels[1] == '1':
                out = 'Backend: '
                if 'backend' in cls.cfg and cls.cfg['backend']:
                    out += 'aktiv'
                else:
                    out += 'nicht aktiv'
                out += '\nFrontend: '
                if 'frontend' in cls.cfg and cls.cfg['frontend']:
                    out += 'aktiv'
                else:
                    out += 'nicht aktiv'
            elif cmd_levels[1] == '2':
                cls.cfg['backend'] = not('backend' in cls.cfg and cls.cfg['backend'])
                cls.sh.cfg.save()
                out = 'Backend: '
                if 'backend' in cls.cfg and cls.cfg['backend']:
                    out += 'aktiv'
                else:
                    out += 'nicht aktiv'
                cls.sh.running = False
        return out
