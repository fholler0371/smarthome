class modul_base:
    def __init__(cls, sh, cfg):
        cls.sh = sh
        cls.cfg = cfg
        cls.running = False

    def start(cls):
        pass

    def stop(cls):
        cls.running = False