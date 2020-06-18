import os
import json

class cfg:
    def __init__(cls, sh, file):
       sh.log.info('__init__')
       cls.sh = sh
       cls.data = {}
       cls.name = sh.basepath+ '/etc/' + file + '.json'
       if not os.path.exists(cls.name):
           if os.path.exists(cls.name+'.default'):
               try:
                   f = open(cls.name+'.default', 'r+')
                   cls.data = json.loads(f.read())
                   f.close()
                   cls.save()
               except:
                   cls.sh.log.error('Fehler beim lesen default:' + cls.name)
           else:
                cls.sh.log.critical('keine Konfiguration:' + cls.name)
           return
       try:
           f = open(cls.name, 'r+')
           cls.data = json.loads(f.read())
           f.close()
       except:
           cls.sh.log.error('Fehler beim lesen:' + cls.name)
       if 'nice' in cls.data:
            del cls.data['nice']
            cls.save()

    def save(cls):
        cls.sh.log.info('save')
        f = open(cls.name, 'w')
        f.write(json.dumps(cls.data, indent=2, sort_keys=True))
        f.close()

def load(sh, file):
    sh.log.info('load: '+file)
    return cfg(sh, file)
