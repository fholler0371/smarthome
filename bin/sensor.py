import time

class sensor:
    def __init__(self):
        self.time = time.time()
        self.name = 'NoName'
        self.value  = None

    def val(self, name, value, rec_time = time.time()):
        self.name = name
        self.value = value
        self.time = rec_time
