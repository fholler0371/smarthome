from threading import Thread, Timer
import time

class timer(Thread):
    def __init__(cls, sh):
        Thread.__init__(cls)
        cls.name = 'timer'
        cls.sh = sh
        cls.sh.log.info("Timer Thred Init")
        cls.sh = sh
        cls.running = False
        cls.timer = None

    def run(cls):
        if not cls.running:
            cls.running = True
            cls.sh.log.info("Timer Thred: Start")
            cls.__loop()
            while cls.running:
                time.sleep(1)
            cls.sh.log.info("Timer Thred: Stop")

    def __loop(cls):
        cls.sh.log.info("Timer Thred: Loop")
        if cls.running:
            wait = (int(time.time()/60)+1)*60-time.time()
            cls.sh.log.debug("wait: "+str(wait))
            cls.timer = Timer(wait, cls.__loop)
            cls.timer.start()

    def stop(cls):
        cls.sh.log.info('Timer Thread: Stopping')
        cls.running = False
        if not cls.timer == None:
            cls.timer.cancel()

def get(sh):
    sh.log.info('get')
    th = timer(sh)
    th.start()
    return th
