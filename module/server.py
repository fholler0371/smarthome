from module import modul_base as base
from threading import Thread
import json
import time, os
import socket
import select

class client(Thread):
    def __init__(cls, sh, conn, ip ,port):
        Thread.__init__(cls)
        sh.log.debug('New server socket thread started for ' + ip + ': ' + str(port))
        cls.sh = sh
        cls.ip = ip
        cls.port = port
        cls.conn = conn
        cls.conn.setblocking(0)
        cls.conn.settimeout(0)
        cls.running = True
        cls.timeout = 120

    def run(cls):
        timer = time.time()
        try:
            while cls.running and timer+cls.timeout > time.time():
                data = cls.conn.recv(2048).decode('ASCII')
                if data == 'HELLO':
                    cls.sh.log.debug('HELLO')
                    cls.conn.send('REMOTE_CLI'.encode('ASCII'))
                    timer = time.time()
                elif data == 'NAME':
                    cls.sh.log.debug('NAME')
                    cls.conn.send(os.uname()[1].encode('ASCII'))
                    timer = time.time()
                elif data == 'MENU':
                    cls.sh.log.debug('MENU')
                    out = {'label': 'Bitte Modul aussuchen', 'entries' : [], 'exit':None}
                    i = 0
                    while i < len(cls.sh.module):
                        if cls.sh.module[i].has_menu:
                             out['entries'].append({'label' : cls.sh.module[i].name, 'cmd': 'MENU '+str(i)})
                        i += 1
                    cls.conn.send(json.dumps(out).encode('ASCII'))
                    timer = time.time()
                elif data == 'EXIT':
                    cls.sh.log.debug('EXIT')
                    cls.running = False
                elif data == '':
                    pass
                else:
                    cls.sh.log.warn('unbekannter Befehl ' + data)
                    cls.conn.send('-'.encode('ASCII'))
                time.sleep(1)
        except Exception as e:
            cls.sh.log.error(str(e))
        cls.conn.close()

class server(Thread):
    def __init__(cls, sh, port):
        Thread.__init__(cls)
        sh.log.info("Server init")
        cls.sh = sh
        cls.running = True
        cls.port = port
        cls.threads = []

    def run(cls):
        try:
            tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcpServer.setblocking(0)
            cls.sh.log.debug('starte Server an Port: '+str(cls.port))
            tcpServer.bind(('0.0.0.0', cls.port))
            tcpServer.listen(5)
            read_list = [tcpServer]
            while cls.running:
                readable, writable, errored = select.select(read_list, [], [], 0)
                for s in readable:
                    if s == tcpServer:
                        (conn, (ip,port)) = tcpServer.accept()
                        th = client(cls.sh, conn, ip, port)
                        th.start()
                        cls.threads.append(th)
                    time.sleep(1)
        except Exception as e:
            cls.sh.log.error(str(e))
        try:
            tcpServer.close()
        except:
            pass
        cls.running = False

    def stop(cls):
        cls.running = False
        try:
            for th in cls.threads:
                th.running = False
        except:
            pass

class modul(base):
    def __init__(cls, sh, cfg):
        base.__init__(cls, sh, cfg)
        cls.sh.log.info('__init__')
        cls.th = None

    def start(cls):
        cls.sh.log.info('start')
        if cls.th == None:
            cls.th = server(cls.sh, cls.cfg['port'])
            cls.th.start()

    def stop(cls):
        cls.sh.log.info('stop')
        if cls.th != None:
            cls.th.stop()
