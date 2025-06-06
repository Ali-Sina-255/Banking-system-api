import logging

from loguru import Logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = Logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_back.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        Logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
