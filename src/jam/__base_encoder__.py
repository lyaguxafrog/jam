# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any


class BaseEncoder(ABC):
    """Base encoder instance."""

    @classmethod
    @abstractmethod
    def dumps(cls, var: dict[str, Any]) -> bytes:
        """Dump dict."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def loads(cls, var: str | bytes) -> dict[str, Any]:
        """Load json."""
        raise NotImplementedError
