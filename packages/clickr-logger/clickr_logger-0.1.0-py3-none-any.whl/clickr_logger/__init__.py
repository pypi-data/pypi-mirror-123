import functools
import logging
import sys
from loguru import logger


__log_format = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'
__sink = None


def logger_wraps(*, entry=True, exit=True, level="DEBUG"):
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(
                    level, "Entering '{}' (args={}, kwargs={})",
                    name, args, kwargs
                )
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


def add_sink(new_sink):
    global __sink
    logger.add(new_sink, format=__log_format)
    __sink = new_sink
    logger.info(f'Configured log {__sink}')


def get_sink():
    global __sink
    return __sink


logger.remove()

logging.getLogger('sh').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
logging.getLogger('selenium').setLevel(logging.INFO)
logging.getLogger('fastapi').setLevel(logging.INFO)

logging.basicConfig(handlers=[InterceptHandler()], level=0)

add_sink(sys.stdout)
