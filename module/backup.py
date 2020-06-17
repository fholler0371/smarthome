class modul:
    def __init__(cls, sh, cfg):
        cls.sh = sh
        cls.cfg = cfg
        cls.sh.log.info('__init__')

    def start(cls):
        cls.sh.log.info('start')
        print(cls.sh)
        print(cls.cfg)

    def stop(cls):
        cls.sh.log.info('stop')
