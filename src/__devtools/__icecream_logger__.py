# -*- coding: utf-8 -*-

from typing import Literal

from icecream import ic

from src.jam.logger import BaseLogger


class IcecreamLogger(BaseLogger):
    """IcecreamLogger is a logger that uses the icecream library to log messages."""

    def __init__(
        self,
        log_level: Literal[
            "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        ] = "INFO",
    ):
        """Initialize the logger."""
        self.log_level = log_level

    def info(self, message):
        """Log an info message."""
        ic(message)

    def error(self, message):
        """Log an error message."""
        ic(message)

    def warning(self, message):
        """Log a warning message."""
        ic(message)

    def debug(self, message):
        """Log a debug message."""
        ic(message)
