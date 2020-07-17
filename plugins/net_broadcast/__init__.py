import time
import socket
import select
from threading import Thread
import json

import plugins

class UDPClient(Thread):
    def __init__(self, sh, port, message):
        Thread.__init__(self)
        self.port = port
        self.message = message
        self.running = True
        self.client = None
        self.resv = []
        self.sh = sh

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
            if len(readable) > 0:
                for sock in readable:
                    if sock == client:
                        data, addr = client.recvfrom(1024)
                        if data == json.dumps({'detect':{}}).encode():
                            self.message['detect_respondse']['friendly_name'] = self.sh.const.friendly_name
                            self.send(json.dumps(self.message))
                        else:
                            try:
                                resv = json.loads(data.decode())
                                self.resv.append(resv)
                            except:
                                pass
            else:
                time.sleep(.1)

    def send(self, message):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client.setblocking(0)
        client.sendto(message.encode(), ("<broadcast>", self.port))

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
        self.th = UDPClient(self.sh, self.cfg['port'], {'detect_respondse':{'name': self.sh.const.server_name,
                                                        'friendly_name': self.sh.const.friendly_name,
                                                        'ip':  self.sh.const.ip.split('/')[0]}})
        self.th.start()

    def stop(self):
        if self.th:
            self.th.running = False

    def scan(self):
        self.th.resv = []
        self.th.send(json.dumps({'detect':{}}))
        time.sleep(2)
        out = []
        for entry in self.th.resv:
           if 'detect_respondse' in entry:
               out.append(entry['detect_respondse'])
        return out
