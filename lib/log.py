import logging

DEFAULT = logging.CRITICAL
stream_handler = None

class MyFormatter(logging.Formatter):
    width = 35
    datefmt='%Y-%m-%d %H:%M:%S'

    def format(cls, record):
        cpath = '%s:%s:%s' % (record.module, record.funcName, record.lineno)
        cpath = cpath[-cls.width:].ljust(cls.width)
        record.message = record.getMessage()
        cls.terminator = '\r'
        s = "%-8s %s %s : %s" % (record.levelname, cls.formatTime(record, cls.datefmt), cpath, record.getMessage())
        return s

def getLogger(name):
    global stream_handler, DEFAULT
    logger = logging.getLogger(name)
    stream_handler = logging.StreamHandler()
    logger.setLevel(DEFAULT)
    formatter = MyFormatter()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

def update(logger, cfg):
    if cfg['level'] == 'debug':
        logger.setLevel(logging.DEBUG)
    if cfg['level'] == 'info':
        logger.setLevel(logging.INFO)
    if cfg['level'] == 'warning':
        logger.setLevel(logging.WARNING)
    if cfg['level'] == 'error':
        logger.setLevel(logging.ERROR)
    if cfg['level'] == 'critical':
        logger.setLevel(logging.CRITICAL)
