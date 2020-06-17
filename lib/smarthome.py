import os, sys, time
import subprocess
import __main__
import psutil
import threading
import lib.log as logging
import lib.config_json as config_json
import lib.module as modul_loader
import lib.timer as timer

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
        cls.timer = timer.get(cls)
        if 'module' in cls.cfg.data:
            for modul in cls.cfg.data['module']:
                m = modul_loader.load(cls.s, modul, cls.cfg.data['module'][modul])
                if not m == None:
                    cls.module.append(m)
                    m.start()

    def run(cls):
        cls.log.info("run")
        timeout = 0
        if 'timeout' in cls.cfg.data:
            timeout = cls.cfg.data['timeout']
        timeout += time.time()
        while cls.is_service or timeout > time.time():
            time.sleep(1)
        for m in cls.module:
            m.stop()
        if not cls.timer == None:
            cls.timer.stop()
        for th in threading.enumerate():
            if not th == threading.main_thread():
                th.join()
        cls.log.info("run beendet")
        print(cls.basepath)
        print(cls.basename)
        print('service:', cls.is_service)

    def __is_service(cls):
        cls.log.info("Check Service")
        return psutil.Process(cls.pid).parent().pid < 5
