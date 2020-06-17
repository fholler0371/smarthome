class modul:
    def __init__(cls, sh, cfg):
        cls.sh = sh
        cls.cfg = cfg
        cls.sh.log.info('__init__')
        print(sh)
        print(cfg)
