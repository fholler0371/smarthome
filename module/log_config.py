from module import modul_base as base

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
