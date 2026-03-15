# -*- coding: utf-8 -*-

from typing import Literal

from icecream import ic

from jam.logger import BaseLogger


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

    def info(self, message: str, *args: object) -> None:  # type: ignore[override]
        """Log an info message."""
        ic(message, *args)

    def error(self, message: str, exc_info: bool = False) -> None:  # type: ignore[override]
        """Log an error message."""
        ic(message)

    def warning(self, message: str, exc_info: bool = False) -> None:  # type: ignore[override]
        """Log a warning message."""
        ic(message)

    def debug(self, message: str, *args: object) -> None:  # type: ignore[override]
        """Log a debug message."""
        ic(message, *args)
