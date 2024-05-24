import logging
import sys

from loguru import logger

from settings import settings


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class CustomLogger:

    @classmethod
    def make_logger(cls):
        logging_config = {
            "level": settings.LOG_LEVEL,
            "format": "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> {extra[request_id]} - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
        }
        return cls.customize_logging(level=logging_config.get('level'), format=logging_config.get('format'))

    @classmethod
    def customize_logging(cls, level: str, format: str):
        logger.remove()
        logger.add(sys.stdout,
                   enqueue=True,
                   backtrace=True,
                   level=level.upper(),
                   format=format)

        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn', 'uvicorn.error', 'fastapi']:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]
        return logger.bind(request_id=None, method=None)


LOGGER = CustomLogger.make_logger()
