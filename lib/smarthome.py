import os, sys, time
import subprocess
import __main__
import psutil
import lib.log as logging
import lib.config_json as config_json
import lib.module as modul_loader

class smarthome:
    def __init__(cls):
        cls.s = cls
        cls.pid = os.getpid()
        f = os.path.abspath(__main__.__file__)
        cls.module = []
        cls.basepath = os.path.dirname(f)
        cls.basename = os.path.splitext(os.path.basename(f))[0]
        cls.log = logging.getLogger(cls.basename)
        cls.is_service = cls.__is_service()
        f = cls.basename
        if not cls.is_service:
            f += '.cmd'
        cls.cfg = config_json.load(cls.s, f)
        if 'logger' in cls.cfg.data:
            logging.update(cls.log, cls.cfg.data['logger'])
        else:
            cls.log.error("kein Eintrag fuer logger in der konfiguration")
        if 'module' in cls.cfg.data:
            for modul in cls.cfg.data['module']:
                m = modul_loader.load(cls.s, modul, cls.cfg.data['module'][modul])
                print(modul)

    def run(cls):
        cls.log.info("run")
        timeout = 0
        if 'timeout' in cls.cfg.data:
            timeout = cls.cfg.data['timeout']
        timeout += time.time()
        while cls.is_service or timeout > time.time():
            time.sleep(1)
        print(cls.basepath)
        print(cls.basename)
        print('service:', cls.is_service)
        cls.log.info("run beendet")

    def __is_service(cls):
        cls.log.info("Check Service")
        return psutil.Process(cls.pid).parent().pid < 5
