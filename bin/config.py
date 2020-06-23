import os
import json

class cfg:
    def __init__(self, sh, file, format= 'json'):
        if hasattr(sh, 'log'):
            sh.log.info('__init__')
        self.sh = sh
        self.data = {}
        self.name = sh.const.path + '/etc/' + file
        if format == 'json':
            self.name += '.json'
        file_name = self.name
        if not os.path.exists(file_name):
            file_name += 'default'
        try:
            f = open(self.name+'.default', 'r+')
            self.data = json.loads(f.read())
            f.close()
        except Exception as e:
            if hasattr(sh, 'log'):
                sh.log.error(str(e))
        if 'nice' in self.data:
             del self.data['nice']
             self.save()

    def save(self):
        if hasattr(self.sh, 'log'):
            self.sh.log.info('save')
        f = open(self.name, 'w')
        f.write(json.dumps(self.data, indent=2, sort_keys=True))
        f.close()

def load(sh, file, format= 'json'):
    if hasattr(sh, 'log'):
        sh.log.info('load: '+file)
    return cfg(sh, file, format)
