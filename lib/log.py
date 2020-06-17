import logging

DEBUG = logging.DEBUG

DEFAULT = DEBUG
stream_handler = None

class MyFormatter(logging.Formatter):
    width = 35
    datefmt='%Y-%m-%d %H:%M:%S'

    def format(cls, record):
        cpath = '%s:%s:%s' % (record.module, record.funcName, record.lineno)
        cpath = cpath[-cls.width:].ljust(cls.width)
        record.message = record.getMessage()
        cls.terminator = '\r'
        s = "%-7s %s %s : %s" % (record.levelname, cls.formatTime(record, cls.datefmt), cpath, record.getMessage())
        return s
#        if record.exc_info:
#           if not record.exc_text:
#                record.exc_text = cls.formatException(record.exc_info)
#        if record.exc_text:
#            if s[-1:] != "\n":
#                s = s + "\n"
#            s = s + record.exc_text

def getLogger(name):
    global stream_handler, DEFAULT
    logger = logging.getLogger(name)
    stream_handler = logging.StreamHandler()
    logger.setLevel(DEFAULT)
    formatter = MyFormatter()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
