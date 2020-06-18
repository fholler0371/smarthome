from module import modul_base as base

class modul(base):
    def __init__(cls, sh, cfg):
        base.__init__(cls, sh, cfg)
        cls.sh.log.info('__init__')
        cls.job_id = -1

    def start(cls):
        cls.sh.log.info('start')
        if "cron" in cls.cfg:
            cls.sh.timer.cron_add(cls.cfg['cron'], cls.backup)

    def stop(cls):
        cls.sh.log.info('stop')


    def backup(cls):
        cls.sh.log.info('backup')
