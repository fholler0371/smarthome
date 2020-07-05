import time
import socket
import select
from threading import Thread

import plugins

class UDPClient(Thread):
    def __init__(self, port, message):
        Thread.__init__(self)
        self.port = port
        self.message = message
        self.running = True

    def run(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client.setblocking(0)
        client.bind(("", self.port))
        read_list = [client]
        while self.running:
            readable, writable, errored = select.select(read_list, [], [], 0)
            for sock in readable:
                if sock == client:
                    data, addr = client.recvfrom(1024)
                    if data == b'HollerHome':
                         client.sendto(self.message.encode(), ("", self.port))
                         print("received message: %s" % data)
            time.sleep(1.1)

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
        self.th = UDPClient(self.cfg['port'], 'ich bin es')
        self.th.start()

    def stop(self):
        if self.th:
            self.th.running = False
