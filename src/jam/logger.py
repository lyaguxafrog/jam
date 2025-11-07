# -*- coding: utf-8 -*-

import logging
from abc import ABC, abstractmethod


class BaseLogger(ABC):
    """Interface for logging."""

    @classmethod
    @abstractmethod
    def info(cls, message: str) -> None:
        """Log an informational message."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def error(cls, message: str) -> None:
        """Log an error message."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def warning(cls, message: str) -> None:
        """Log a warning message."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def debug(cls, message: str) -> None:
        """Log a debug message."""
        raise NotImplementedError


class JamLogger(BaseLogger):
    """Default jam logger, use stdlib logging."""

    def __init__(self):
        """Initialize the logger."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
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
