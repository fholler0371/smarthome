#!/media/pi/data/SM/smarthome/env/bin/python3

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Version 1.0
"""

import os, sys
import socket
import json
import netifaces
from bin import ping
from bin import menu_cli
from bin import log as logging
from bin import config_json
import __main__

class client_cls:
    def __init__(cls):
        f = os.path.abspath(__main__.__file__)
        cls.basepath = os.path.dirname(f)
        cls.basename = os.path.splitext(os.path.basename(f))[0]
        cls.log = logging.getLogger(cls.basename)
        f = cls.basename
        cls.cfg = config_json.load(cls, f)
        if cls.cfg.data['ip'] == '':
            cls.__guess_network()
            cls.cfg.save()
        if 'logger' in cls.cfg.data:
            logging.update(cls, cls.log, cls.cfg.data['logger'])

    def __guess_network(cls):
        net = []
        for interface in netifaces.interfaces():
            if 'broadcast' in netifaces.ifaddresses(interface)[netifaces.AF_INET][0]:
                net.append(interface)
        gw = netifaces.gateways()['default'][netifaces.AF_INET][1]
        interface = None
        if len(net) > 1:
            for i in net:
                if str(i) != str(gw):
                    interface = i
        elif len(net) > 0:
            interface = net[0]
        if interface == None:
            print('kein Netzwerk gefunden')
            sys.exit()
        addr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
        cls.cfg.data['ip'] = addr['addr'] + '/' + addr['netmask']

def get_cmd(log, host, port, cmd):
    log.info(cmd)
    print('')
    print('Befehl gesendet')
    print('')
    dataj = None
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((str(host['ip']), port))
        s.send(cmd.encode('ascii'))
        value = ''
        while not value.endswith('>>END<<'):
            data = s.recv(1024)
            value += data.decode('ascii')
        s.close()
    except Exception as e:
        log.error(str(e))
    print(value[:-7])
    print('')
    input('Bitte eine Taste druecken')

def get_menu(log, host, port, cmd):
    log.info(cmd)
    dataj = None
    out = None
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((str(host['ip']), port))
        s.send(cmd.encode('ascii'))
        data = s.recv(1024)
        dataj = json.loads(data.decode('ascii'))
        s.close()
    except Exception as e:
        print(data)
        log.error(str(e))
    if dataj != None:
        while str(out) != '-1':
            out = menu_cli.menu({"exit":"Zurueck","titel": dataj['label'], "entries2":dataj['entries']})
            if out != -1:
                if out.startswith('CMD'):
                    get_cmd(log, host, port, out)
                else:
                   get_menu(log, host, port, out)

def connect_host(log, host, port):
    log.info('connect ' + host['ip'] + ' port: ' + str(port))
    get_menu(log, host, port, 'MENU')

def Main():
    client = client_cls()
    hosts = []
    for host in ping.scan(client.log, client.cfg.data['ip']):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((str(host),client.cfg.data['port']))
            message = 'HELLO'
            s.send(message.encode('ascii'))
            data = s.recv(1024)
            if 'REMOTE_CLI' == data.decode('ascii'):
                s.send('NAME'.encode('ascii'))
                hosts.append({'ip': host, 'name': s.recv(1024).decode('ascii')})
            s.close()
        except Exception as e:
           client.log.debug(str(e))
    data = []
    for host in hosts:
        data.append(host['name'])
    out = 0
    while out != -1:
       out = menu_cli.menu({'exit"': 'Beenden', 'titel': 'Bitte einen Server aussuchen', 'entries':data})
       if out > 0:
           connect_host(client.log, hosts[out-1], client.cfg.data['port'])

if __name__ == '__main__':
	Main()

