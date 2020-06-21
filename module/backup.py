from module import modul_base as base

class modul(base):
    def __init__(cls, sh, cfg):
        base.__init__(cls, sh, cfg)
        cls.sh.log.info('__init__')
        cls.has_menu = True
        cls.name = "Backup"

    def start(cls):
        cls.sh.log.info('start')
        if "cron" in cls.cfg:
            cls.sh.timer.cron_add(cls.cfg['cron'], cls.backup)

    def stop(cls):
        cls.sh.log.info('stop')


    def backup(cls):
        cls.sh.log.info('backup')

    def menu_cli(cls, menu):
        cls.sh.log.info('menu_cli')
        cls.sh.log.debug(menu)
        out = '-'
        menu_levels = menu[5:].split('.')
        if len(menu_levels) == 1:
            out = json.dumps({'label': 'Bitte Aktion aussuchen', 'entries' : [
                {'label' : 'Status', 'cmd': 'CMD ' + str(menu_levels[0]) + '.1'},
                {'label' : 'Cronzeit einstellen', 'cmd': 'MENU ' + str(menu_levels[0]) + '.1'}
                ], 'exit':None})
