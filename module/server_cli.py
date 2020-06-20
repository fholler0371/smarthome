from module import modul_base as base
import json
import subprocess

class modul(base):
    def __init__(cls, sh, cfg):
        base.__init__(cls, sh, cfg)
        cls.sh.log.info('__init__')
        cls.has_menu = True
        cls.name = 'Server Commandos'

    def start(cls):
        cls.sh.log.info('start')

    def stop(cls):
        cls.sh.log.info('stop')

    def menu_cli(cls, menu):
        cls.sh.log.info('menu_cli')
        cls.sh.log.debug(menu)
        out = '-'
        menu_levels = menu[5:].split('.')
        if len(menu_levels) == 1:
            out = json.dumps({'label': 'Bitte Modul aussuchen', 'entries' : [
                {'label' : 'Sytemupdate', 'cmd': 'CMD ' + str(menu_levels[0]) + '.1'},
                {'label' : 'Reboot', 'cmd': 'CMD ' + str(menu_levels[0]) + '.2'}
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
                response1 = subprocess.Popen(('sudo apt-get update').split(' '), stdout=subprocess.PIPE).stdout.read()
                out = response1.decode(errors= 'backslashreplace')
                response2 = subprocess.Popen(('sudo apt-get upgrade -y').split(' '), stdout=subprocess.PIPE).stdout.read()
                out += response2.decode(errors= 'backslashreplace')
            elif cmd_levels[1] == '2':
                response1 = subprocess.Popen(('sudo reboot').split(' '), stdout=subprocess.PIPE).stdout.read()
                out = response1.decode(errors= 'backslashreplace')
        return out
