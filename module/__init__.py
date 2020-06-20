class modul_base:
    def __init__(cls, sh, cfg):
        cls.sh = sh
        cls.cfg = cfg
        cls.running = False
        cls.has_menu = False
        cls.name = 'Noname'

    def start(cls):
        pass

    def stop(cls):
        cls.running = False

    def menu_cli(cls, menu):
        return '-'
