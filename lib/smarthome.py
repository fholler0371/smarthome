import os, sys
import subprocess
import __main__
import psutil
import lib.log as logging
import lib.config_json as config_json

class smarthome:
    def __init__(cls):
        cls.s = cls
        cls.pid = os.getpid()
        f = os.path.abspath(__main__.__file__)
        cls.basepath = os.path.dirname(f)
        cls.basename = os.path.splitext(os.path.basename(f))[0]
        cls.log = logging.getLogger(cls.basename)
        cls.is_service = cls.__is_service()
        f = cls.basename
        if not cls.is_service:
            f += '.cmd'
        cls.cfg = config_json.load(cls, f)
        if 'logger' in cls.cfg.data:
            logging.update(cls.log, cls.cfg.data['logger'])
        else:
            cls.log.error("kein Eintrag fuer logger in der konfiguration")

    def run(cls):
        cls.log.info("run")
        print(cls.basepath)
        print(cls.basename)
        print('service:', cls.is_service)

    def __is_service(cls):
        cls.log.info("Check Service")
        return psutil.Process(cls.pid).parent().pid < 5
