from threading import Thread, Timer
import random

import plugins

class timer(Thread):
    def __init__(self, intervall, job):
        Thread.__init__(self)
        self.intervall = intervall
        self.job = job
        self.running = False
        self.timer = None

    def run(self):
        if not self.running:
           self.running = True
           self.timer  = Timer(0.1 * self.intervall, self.do)
           self.timer.start()

    def do(self):
        if self.running:
           self.timer  = Timer((0.9+0.2*random.random()) * self.intervall, self.do)
           self.timer.start()
           self.job()

    def stop(self):
        self.running = False
        if self.timer:
            self.timer.cancel()

class plugin(plugins.base):
    def __init__(self, sh, name):
        plugins.base.__init__(self, sh, name)
        self.sh.log.info(name + '__init__')
        val = {}
        self.create_config(val)
        self.loaded = True
        self.th = []
        self.sh.plugins.register(self)

    def start(self, intervall, job):
        th = timer(intervall, job)
        th.start()
        self.th.append(th)
        return th

    def stop(self):
        for th in self.th:
            th.stop()
