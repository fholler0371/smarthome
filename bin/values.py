import os
import __main__

import psutil

class basic():
    def __init__(self):
        self.pid = os.getpid()
        self.is_service = psutil.Process(self.pid).parent().pid < 5
        file = os.path.abspath(__main__.__file__)
        self.path = os.path.dirname(file)
        self.name = os.path.splitext(os.path.basename(file))[0]
