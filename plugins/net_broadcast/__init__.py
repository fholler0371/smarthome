import time
import socket
import select
from threading import Thread
import json

import plugins

class UDPClient(Thread):
    def __init__(self, port, message):
        Thread.__init__(self)
        self.port = port
        self.message = message
        self.running = True
        self.client = None

    def run(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client.setblocking(0)
        client.bind(("", self.port))
        read_list = [client]
        self.client = client
        while self.running:
            readable, writable, errored = select.select(read_list, [], [], 0)
            for sock in readable:
                if sock == client:
                    data, addr = client.recvfrom(1024)
                    if data == b'HollerHome':
                         self.send(self.message)
                         print("received message: %s" % data)
                    else:
                         print("received xxx: %s" % data)
            time.sleep(1.1)

    def send(self, message):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client.setblocking(0)
        client.sendto(message.encode(), ("", self.port))

class plugin(plugins.base):
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')

        self.th = None

        ''' Prüfen der Konfig und sezen ggf. der defaults'''
        val = {
            'port' : 4111
          }
        self.create_config(val)

        ''' setzten und pruefen der Abhaengigkeiten '''
        self.require = []
        self.get_requirements()

        ''' wenn alles Ok Plugin registrieren '''
        if self.loaded:
            self.sh.plugins.register(self)

    def run(self):
        self.th = UDPClient(self.cfg['port'], json.dumps({'name': self.sh.const.server_name,
                                                          'ip':  self.sh.const.ip.split('/')[0]}))
        self.th.start()

    def stop(self):
        if self.th:
            self.th.running = False

    def scan(self):
        self.th.send('HollerHome')
