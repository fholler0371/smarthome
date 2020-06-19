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

import __main__
import os, sys, time
import bin.log as logging
import bin.config_json as config_json

basepath = os.path.dirname(os.path.abspath(__main__.__file__))
sys.path.append(basepath+"/lib")

import config
import ipaddress
import socket
import ping
import subprocess
import menu_cli

# Import socket module
import time

class client_cls:
    def __init__(cls):
        f = os.path.abspath(__main__.__file__)
        cls.basepath = os.path.dirname(f)
        cls.basename = os.path.splitext(os.path.basename(f))[0]
        cls.log = logging.getLogger(cls.basename)
        f = cls.basename
        cls.cfg = config_json.load(cls, f)

def connect_service(host, service):
	menu_id = 0
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((str(host["ip"]),service["port"]))
		message = "MENU "+str(menu_id)
		s.send(message.encode('ascii'))
		data = s.recv(1024)
		print(data)
		s.close()
	except:
		pass
	print(host)
	print(service)
	input("halt")

def connect_host(host, port):
	services = []
	i = 0
	while i < 50:
		try:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.settimeout(2)
			s.connect((str(host["ip"]),port+i))
			message = "HELLO"
			s.send(message.encode('ascii'))
			data = s.recv(1024)
			services.append({"port": port+i, "name": data.decode('ascii')})
			s.close()
		except:
			pass
		i += 1
	data = []
	for x in services:
		data.append(x["name"])
	out = 0
	while not(out == -1):
		out = menu_cli.menu({"exit":"Beenden","titel":"Bitte einen Service vom Rechner "+host["name"]+" aussuchen", "entries":data})
		if out > 0:
			connect_service(host, services[out-1])

def Main():
    client = client_cls()
    print(client.basepath)
    print(client.basename)
    print(client.basename)
    print(client.cfg.data)
    return

def x():
	cfg = config.c_config()
	cfg.load(basepath+"/cfg/"+os.path.splitext(os.path.basename(main_lib.__file__))[0]+".json")
	print("Suche Rechner")
	hosts = []
	for host in ping.scan(cfg.data["ip-range"]):
		try:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.settimeout(2)
			s.connect((str(host),cfg.data["port"]))
			message = "HELLO"
			s.send(message.encode('ascii'))
			data = s.recv(1024)
			if "REMOTE_CLI" == data.decode('ascii'):
				s.send("NAME".encode('ascii'))
				hosts.append({"ip": host, "name": s.recv(1024).decode('ascii')})
			s.close()
		except:
			pass
	data = []
	for x in hosts:
		data.append(x["name"])
	out = 0
	while not(out == -1):
		out = menu_cli.menu({"exit":"Beenden","titel":"Bitte einen Server aussuchen", "entries":data})
		if out > 0:
			connect_host(hosts[out-1], cfg.data["port"])

if __name__ == '__main__':
	Main()

