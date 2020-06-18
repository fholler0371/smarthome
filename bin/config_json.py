import os
import json

class cfg:
    def __init__(cls, sh, file):
       sh.log.info('__init__')
       cls.sh = sh
       cls.data = {}
       cls.name = sh.basepath+ '/cfg/' + file + '.json'
       if not os.path.exists(cls.name):
           cls.sh.log.critical('keine Konfiguration:' + cls.name)
           return
       try:
           f = open(cls.name, 'r+')
           cls.data = json.loads(f.read())
           f.close()
       except:
           cls.sh.log.error('Fehler beim lesen:' + cls.name)

def load(sh, file):
    sh.log.info('load: '+file)
    return cfg(sh, file)
