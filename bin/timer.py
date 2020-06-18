from threading import Timer
import time
import cronex

class timer:
    def __init__(cls, sh):
        cls.sh = sh
        cls.sh.log.info("Init")
        cls.sh = sh
        cls.running = False
        cls.timer = None
        cls.cron = []

    def start(cls):
        cls.sh.log.info("Start")
        if not cls.running:
            cls.running = True
            cls.__loop()

    def __loop(cls):
        cls.sh.log.info("Loop")
        if cls.running:
            wait = (int(time.time()/60)+1)*60-time.time()
            cls.sh.log.debug("wait: "+str(wait))
            cls.timer = Timer(wait, cls.__loop)
            cls.timer.start()
            for cron in cls.cron:
                job = cronex.CronExpression(cron["pattern"])
                if job.check_trigger(time.localtime(time.time())[:5]):
                     cls.sh.log.debug("call: "+str(cron))
                     cron['job']()

    def stop(cls):
        cls.sh.log.info('Timer Thread: Stopping')
        cls.running = False
        if not cls.timer == None:
            cls.timer.cancel()

    def cron_add(cls, pattern, job):
        cls.sh.log.info('add cron job')
        cls.sh.log.debug(pattern + " " + str(job))
        cls.cron.append({'pattern': pattern, 'job': job})

def get(sh):
    sh.log.info('get')
    th = timer(sh)
    th.start()
    return th
