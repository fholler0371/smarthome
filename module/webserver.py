import json
from module import modul_base as base

class modul(base):
    def __init__(cls, sh, cfg):
        base.__init__(cls, sh, cfg)
        cls.sh.log.info('__init__')
        cls.name = "WebServer"
        cls.has_menu = True

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
                {'label' : 'Status', 'cmd': 'CMD ' + str(menu_levels[0]) + '.1'},
                {'label' : 'Backend aktivieren/deaktivieren', 'cmd': 'CMD ' + str(menu_levels[0]) + '.2'},
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
                out = 'Backend: '
                if 'backend' in cls.cfg and cls.cfg['backend']:
                    out += 'aktiv'
                else:
                    out += 'nicht aktiv'
                out += '\nFrontend: '
                if 'frontend' in cls.cfg and cls.cfg['frontend']:
                    out += 'aktiv'
                else:
                    out += 'nicht aktiv'
            elif cmd_levels[1] == '2':
                cls.cfg['backend'] = not('backend' in cls.cfg and cls.cfg['backend'])
                cls.sh.cfg.save()
                out = 'Backend: '
                if 'backend' in cls.cfg and cls.cfg['backend']:
                    out += 'aktiv'
                else:
                    out += 'nicht aktiv'
                cls.sh.running = False
        return out
