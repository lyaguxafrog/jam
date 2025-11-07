# -*- coding: utf-8 -*-

from icecream import ic

from jam.logger import BaseLogger


class IcecreamLogger(BaseLogger):
    """Debug icecream logger."""

    def __init__(self):
        """Init."""
        self._logger = ic

    def debug(self, message):
        """Debug message."""
        self._logger(message)

    def info(self, message):
        """Info message."""
        self._logger(message)

    def warning(self, message):
        """Warning message."""
        self._logger(message)

    def error(self, message):
        """Error message."""
        self._logger(message)

    def critical(self, message):
        """Critical message."""
        self._logger(message)

    def exception(self, message):
        """Exception message."""
        self._logger(message)

    def log(self, level, message):
        """Log message."""
        self._logger(message)
