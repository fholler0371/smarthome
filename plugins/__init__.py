class master():
    def __init__(self, sh):
        self.sh = sh
        self.sh.plugins = self
        self.plugins = []

class base():
    def __init__(self):
        self.requirements = []
