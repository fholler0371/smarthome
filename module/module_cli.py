import json
from module import modul_base as base

class modul(base):
    def __init__(cls, sh, cfg):
        base.__init__(cls, sh, cfg)
        cls.sh.log.info('__init__')
        cls.has_menu = True
        cls.name = 'Module aktivieren/deaktivieren'


    def start(cls):
        cls.sh.log.info('start')
        if "cron" in cls.cfg:
            cls.sh.timer.cron_add(cls.cfg['cron'], cls.backup)

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
                {'label' : 'Aktivieren', 'cmd': 'MENU ' + str(menu_levels[0]) + '.1'},
                {'label' : 'Deaktivieren', 'cmd': 'MENU ' + str(menu_levels[0]) + '.2'}
                ], 'exit':None})
        elif len(menu_levels) == 2:
            if menu_levels[1] == '1':
                data = {'label': 'Bitte Modul aktivie', 'entries' : [], 'exit':None}
                for modul in cls.sh.cfg.data['module']:
                    if not cls.sh.cfg.data['module'][modul]['active']:
                        data['entries'].append({'label': modul, 'cmd': 'CMD ' +  str(menu_levels[0]) + '.2.' + modul})
                out = json.dumps(data)
            elif menu_levels[1] == '2':
                data = {'label': 'Bitte Modul deaktivie', 'entries' : [], 'exit':None}
                for modul in cls.sh.cfg.data['module']:
                    if cls.sh.cfg.data['module'][modul]['active']:
                        data['entries'].append({'label': modul, 'cmd': 'CMD ' +  str(menu_levels[0]) + '.3.' + modul})
                out = json.dumps(data)
        return out

    def cmd_cli(cls, cmd):
        cls.sh.log.info('cmd_cli')
        cls.sh.log.debug(cmd)
        out = '-'
        cmd_levels = cmd[4:].split('.')
        if len(cmd_levels) == 1:
            return out
        elif len(cmd_levels) > 1:
            if cmd_levels[1] == '1':
                out = ''
                for modul in cls.sh.cfg.data['module']:
                    if cls.sh.cfg.data['module'][modul]['active']:
                        out += '+ '
                    else:
                        out += '- '
                    out += modul + '\n'
            elif cmd_levels[1] == '2':
                cls.sh.cfg.data['module'][cmd_levels[2]]['active'] = True
                cls.sh.cfg.save()
                out = cmd_levels[2] + 'ist aktiviert, es wird neu laden'
                cls.sh.running = False
            elif cmd_levels[1] == '3':
                cls.sh.cfg.data['module'][cmd_levels[2]]['active'] = False
                cls.sh.cfg.save()
                out = cmd_levels[2] + 'ist aktiviert, es wird neu laden'
                cls.sh.running = False
        return out
