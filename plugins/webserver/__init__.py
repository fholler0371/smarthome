import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
from threading import Thread
from functools import partial

import plugins

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class webserverHandler(BaseHTTPRequestHandler):
    def __init__(self, sh, path, lib, qux, *args, **kwargs):
        self.sh = sh
        self.root_path = path
        self.root_lib = lib
        self.qux = qux
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        self.sh.log.info("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(),format%args))

    def do_GET(self):
        path = self.path
        if path.endswith('/'):
            path += 'index.html'
        if path.startswith('/lib/'):
            path = self.sh.const.path + '/' + self.root_lib + '/' + path[5:]
        else:
            path = self.sh.const.path + '/' + self.root_path + '/' + path[1:]
        path = path.replace('/./', '/').replace('/../', '/').replace('//', '/')
        if not os.path.exists(path):
            self.send_response(404)
            self.send_header('Content-Type',
                             'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('error 404'.encode('utf-8'))
            return
        self.send_response(200)
        if path.endswith('.html'):
            self.send_header('Content-Type',
                             'text/html; charset=utf-8')
            self.end_headers()
            file = open(path, 'rb')
            self.wfile.write(file.read())
            file.close()
        elif path.endswith('.js'):
            self.send_header('Content-Type',
                             'application/javascript')
            self.end_headers()
            file = open(path, 'rb')
            self.wfile.write(file.read())
            file.close()
        elif path.endswith('.css'):
            self.send_header('Content-Type',
                             'text/css')
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
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        self.server.serve_forever()

class plugin(plugins.base):
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')
        self.loaded = True
        self.sh.plugins.plugins[name] = self

    def webserver_run(self, port, path, lib):
        self.sh.log.info('webserver_run')
        print(port)
        handler = partial(webserverHandler, self.sh, path, lib, self)
        server = ThreadedHTTPServer(('0.0.0.0', port), handler)
        th = loopThread(server)
        th.start()
        return server
