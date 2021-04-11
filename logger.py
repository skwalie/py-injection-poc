import logging
import logging.config


class Logger(object):
    def debug(self, msg, *args, **kwargs):
        pass

    def info(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass


class DefaultLogger(Logger):
    def __init__(self):
        self._logging = logging
        self._logging.config.fileConfig("logging.conf")

    def debug(self, msg, *args, **kwargs):
        self._logging.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logging.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logging.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logging.error(msg, *args, **kwargs)
