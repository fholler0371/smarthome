import os
import sys
import time
import subprocess
import psutil

def call(sh, data):
    print("System Call")
    if 'client_get_state' == data['data']['cmd']:
        return get_state(sh)
    elif 'client_get_var' == data['data']['cmd']:
        return get_var(sh)
    print(data['data'])
    return data['data']

def get_var(sh):
   out = {'master': False, 'geo': {'lat': 52.5092947, 'long': 13.4178536}}
   if hasattr(sh.const, 'geo'):
       out['geo'] = sh.const.geo
   out['master'] = sh.const.master
   out['friendly_name'] = sh.const.friendly_name
   return out


def get_state(sh):
    out = {}
    response = subprocess.Popen(('cat /sys/firmware/devicetree/base/model').split(' '), stdout=subprocess.PIPE).stdout.read()
    out['type'] = response.decode(errors= 'backslashreplace')
    response = subprocess.Popen(('cat /proc/meminfo').split(' '), stdout=subprocess.PIPE).stdout.read().decode().split('\n')
    value = response[0]
    while value.find('  ') > -1:
        value = value.replace('  ', ' ')
    value = int(value.split(' ')[1])/1024/1024
    value = ("{:.3f}".format(value)).replace('.', ',') + ' GiB'
    out['mem'] = value
    value = response[1]
    while value.find('  ') > -1:
        value = value.replace('  ', ' ')
    value = int(value.split(' ')[1])/1024/1024
    value = ("{:.3f}".format(value)).replace('.', ',') + ' GiB'
    out['free'] = value
    response = subprocess.Popen(('cat /sys/class/thermal/thermal_zone0/temp').split(' '), stdout=subprocess.PIPE).stdout.read()
    out['temp'] = ("{:.1f}".format(int(response.decode())/1000)).replace('.', ',')+' C'
    out['hostname'] = os.uname()[1]
    value = psutil.disk_usage(sh.const.path)
    out['disk'] = ("{:.2f}".format(value.free/1024/1024/1024)).replace('.', ',') + ' GiB '
    out['disk'] += ("{:.1f}".format(100-value.percent)).replace('.', ',') + '%'
    value = int(time.time() - psutil.boot_time())
    out['uptime'] = ('0'+str(value % 60))[-2:]
    value = int(value/60)
    out['uptime'] = ('0'+str(value % 60))[-2:] + ':' + out['uptime']
    value = int(value/60)
    out['uptime'] = ('0'+str(value % 24))[-2:] + ':' + out['uptime']
    value = int(value/24)
    if value > 0:
        out['uptime'] = str(value) + 'd ' + out['uptime']
    value = int(time.time() - sh.const.start_time)
    out['shtime'] = ('0'+str(value % 60))[-2:]
    value = int(value/60)
    out['shtime'] = ('0'+str(value % 60))[-2:] + ':' + out['shtime']
    value = int(value/60)
    out['shtime'] = ('0'+str(value % 24))[-2:] + ':' + out['shtime']
    value = int(value/24)
    if value > 0:
        out['shtime'] = str(value) + 'd ' + out['shtime']
    response = subprocess.Popen(('uname -r').split(' '), stdout=subprocess.PIPE).stdout.read()
    out['kernalversion'] = response.decode(errors= 'backslashreplace').split('\n')[0]
    response = subprocess.Popen(('cat /etc/os-release').split(' '), stdout=subprocess.PIPE).stdout.read()
    out['osname'] = response.decode(errors= 'backslashreplace').split('"')[1]
    out['python'] = sys.version.split(' ')[0]
    out['serial'] = sh.const.serial
    out['version'] = sh.const.version
    out['ip'] = sh.const.ip.split('/')[0]
    out['last'] = subprocess.Popen(('cat /proc/loadavg').split(' '), stdout=subprocess.PIPE).stdout.read().decode().split(' ')[2].replace('.', ',')
    return out
