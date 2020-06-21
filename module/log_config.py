import json
from module import modul_base as base
import bin.log as logging

class modul(base):
    def __init__(cls, sh, cfg):
        base.__init__(cls, sh, cfg)
        cls.sh.log.info('__init__')
        cls.has_menu = True
        cls.name = "Logger"

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
            out = json.dumps({'label': 'Bitte Aktion aussuchen', 'entries' : [
                {'label' : 'Status', 'cmd': 'CMD ' + str(menu_levels[0]) + '.1'},
                {'label' : 'Ziel aendern', 'cmd': 'MENU ' + str(menu_levels[0]) + '.1'},
                {'label' : 'Level waelen', 'cmd': 'MENU ' + str(menu_levels[0]) + '.2'}
                ], 'exit':None})
        elif len(menu_levels) == 2:
            if menu_levels[1] == '1':
                out = json.dumps({'label': 'Bitte Ziel aussuchen', 'entries' : [
                    {'label' : 'Konsole', 'cmd': 'CMD ' + str(menu_levels[0]) + '.2'},
                    {'label' : 'Datei', 'cmd': 'CMD ' + str(menu_levels[0]) + '.3'}
                    ], 'exit':None})
            elif menu_levels[1] == '2':
                out = json.dumps({'label': 'Bitte Level aussuchen', 'entries' : [
                    {'label' : 'CRITICAL', 'cmd': 'CMD ' + str(menu_levels[0]) + '.4'},
                    {'label' : 'ERROR', 'cmd': 'CMD ' + str(menu_levels[0]) + '.5'},
                    {'label' : 'WARNING', 'cmd': 'CMD ' + str(menu_levels[0]) + '.6'},
                    {'label' : 'INFO', 'cmd': 'CMD ' + str(menu_levels[0]) + '.7'},
                    {'label' : 'DEBUG', 'cmd': 'CMD ' + str(menu_levels[0]) + '.8'}
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
                out = ''
                try:
                    out += 'Ziel: ' + str(cls.sh.cfg.data['logger']['dest']) + '\n'
                    out += 'Level: ' + str(cls.sh.cfg.data['logger']['level']) + '\n'
                except:
                    pass
            elif cmd_levels[1] == '2':
                cls.sh.cfg.data['logger']['dest'] = 'console'
            elif cmd_levels[1] == '3':
                cls.sh.cfg.data['logger']['dest'] = 'file'
            elif cmd_levels[1] == '4':
                cls.sh.cfg.data['logger']['level'] = 'critical'
            elif cmd_levels[1] == '5':
                cls.sh.cfg.data['logger']['level'] = 'error'
            elif cmd_levels[1] == '6':
                cls.sh.cfg.data['logger']['level'] = 'warning'
            elif cmd_levels[1] == '7':
                cls.sh.cfg.data['logger']['level'] = 'info'
            elif cmd_levels[1] == '8':
                cls.sh.cfg.data['logger']['level'] = 'debug'
            if int(cmd_levels[1]) > 1:
                cls.sh.cfg.save()
                logging.update(cls.sh, cls.sh.log, cls.sh.cfg.data['logger'])
            return out
