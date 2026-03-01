# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import logging
import os
from typing import Any, Literal


class BaseLogger(ABC):
    """Interface for logging."""

    _LOG_NAME: str = "jam"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @abstractmethod
    def info(self, message: str) -> None:
        """Log an informational message."""
        raise NotImplementedError

    @abstractmethod
    def error(self, message: str, exc_info: bool = False) -> None:
        """Log an error message.

        Args:
            message (str): Error message
            exc_info (bool): Whether to include exception info
        """
        raise NotImplementedError

    @abstractmethod
    def warning(self, message: str, exc_info: bool = False) -> None:
        """Log a warning message.

        Args:
            message (str): Warning message
            exc_info (bool): Whether to include exception info
        """
        raise NotImplementedError

    @abstractmethod
    def debug(self, message: str, *args: Any) -> None:
        """Log a debug message."""
        raise NotImplementedError


class JamLogger(BaseLogger):
    """Default jam logger, use stdlib logging."""

    _LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

    def __init__(
        self,
        log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        | str = "INFO",
    ):
        """Initialize the logger."""
        if log_level not in self._LOG_LEVELS:
            log_level = "INFO"
        self.logger = logging.getLogger(self._LOG_NAME)
        self.logger.setLevel(log_level)
        if not self.logger.handlers:
            self.logger.addHandler(logging.NullHandler())

    def info(self, message: str) -> None:
        """Log an informational message."""
        self.logger.info(message)

    def error(self, message: str, exc_info: bool = False) -> None:
        """Log an error message.

        Args:
            message (str): Error message
            exc_info (bool): Whether to include exception info
        """
        self.logger.error(message, exc_info=exc_info)

    def warning(self, message: str, exc_info: bool = False) -> None:
        """Log a warning message.

        Args:
            message (str): Warning message
            exc_info (bool): Whether to include exception info
        """
        self.logger.warning(message, exc_info=exc_info)

    def debug(self, message: str, *args: Any) -> None:
        """Log a debug message."""
        if args:
            self.logger.debug(message, *args)
        else:
            self.logger.debug(message)

    def __str__(self) -> str:
        """Return a string representation of the logger."""
        return f"JamLogger({self.logger.name})"

    def __repr__(self) -> str:
        """Return a string representation of the logger."""
        return f"JamLogger({self.logger.name})"


logger = JamLogger(os.getenv("JAM_LOG_LEVEL", "INFO").upper())
