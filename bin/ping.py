import subprocess
from threading import Thread
import ipaddress
import time

import netifaces

send = 0
receive = 0
hosts = []
logger = None

def set_zero():
    global send, receive
    send = 0
    receive = 0

def succsess(host):
    global receive, hosts, logger
    logger.debug('found: ' + host)
    receive += 1
    hosts.append(host)

def fail():
    global receive
    receive += 1

class do_ping(Thread):
    def __init__(cls, log, host, succsess, fail):
        Thread.__init__(cls)
        cls.host = host
        cls.succsess = succsess
        cls.fail = fail

    def run(cls):
        ping_response = subprocess.Popen(['/bin/ping', '-c1', '-W1', str(cls.host)], stdout=subprocess.PIPE).stdout.read()
        if ping_response.decode().find("1 received") > 0:
            cls.succsess(cls.host)
        else:
           cls.fail()

def scan(log, range):
    log.info('Scan Netzwerk')
    global send, receive
    timeout = 0
    set_zero()
    net = ipaddress.ip_network(range, False)
    for host in net:
        timeout += 0.5
        ping(log, str(host))
        timeout += time.time()
    while timeout > time.time() and (send - receive) > 0:
        time.sleep(0.5)
    return hosts

def guess_network():
    net = []
    for interface in netifaces.interfaces():
        if netifaces.AF_INET in netifaces.ifaddresses(interface) and 'broadcast' in netifaces.ifaddresses(interface)[netifaces.AF_INET][0]:
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
        return ''
    addr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
    return addr['addr'] + '/' + addr['netmask']

def is_ip_in_range(range, ip):
    res = False
    net = ipaddress.ip_network(range, False)
    for host in net:
        if ip == str(host):
            res = True
    return res

def ping(log, host):
    log.info('Ping: '+host)
    global logger
    logger = log
    global send, receive, hosts
    send += 1
    if not(host.split('.')[3] == '0') and not(host.split('.')[3] == '255'):
        th = do_ping(log, host, succsess, fail)
        th.start()
    else:
        receive += 1
