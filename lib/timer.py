from threading import Thread
import time

class timer(Thread):
    def __init__(cls, sh):
        Thread.__init__(cls)
        cls.name = 'timer'
        cls.sh = sh
        cls.sh.log.info("Timer Thred Init")
        cls.sh = sh
        cls.running = False

    def run(cls):
        if not cls.running:
            cls.running = True
            cls.sh.log.info("Timer Thred: Start")
            while cls.running:
                time.sleep(1)
            cls.sh.log.info("Timer Thred: Stop")


    def stop(cls):
        cls.sh.log.info('Timer Thread: Stopping')
        cls.running = False

def get(sh):
    sh.log.info('get')
    th = timer(sh)
    th.start()
    return th
