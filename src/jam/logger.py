# -*- coding: utf-8 -*-

import logging
from abc import ABC, abstractmethod
from typing import Literal


class BaseLogger(ABC):
    """Interface for logging."""

    @abstractmethod
    def info(cls, message: str) -> None:
        """Log an informational message."""
        raise NotImplementedError

    @abstractmethod
    def error(cls, message: str) -> None:
        """Log an error message."""
        raise NotImplementedError

    @abstractmethod
    def warning(cls, message: str) -> None:
        """Log a warning message."""
        raise NotImplementedError

    @abstractmethod
    def debug(cls, message: str) -> None:
        """Log a debug message."""
        raise NotImplementedError


class JamLogger(BaseLogger):
    """Default jam logger, use stdlib logging."""

    def __init__(
        self,
        log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    ):
        """Initialize the logger."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        self.logger.addHandler(handler)

    def info(self, message: str) -> None:
        """Log an informational message."""
        self.logger.info(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)

    def __str__(self) -> str:
        """Return a string representation of the logger."""
        return f"JamLogger({self.logger.name})"

    def __repr__(self) -> str:
        """Return a string representation of the logger."""
        return f"JamLogger({self.logger.name})"


logger = JamLogger("INFO")
