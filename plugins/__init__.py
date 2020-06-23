class master():
    def __init__(self, sh):
        sh.log.info('init master')
        self.sh = sh
        self.sh.plugins = self
        self.plugins = []

    def load(self, in_data):
        sh.log.info('load master')
        print(typeof(in_data))

class base():
    def __init__(self):
        self.requirements = []
