# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Union


class BaseEncoder(ABC):
    """Base encoder instance."""

    @classmethod
    @abstractmethod
    def dumps(cls, var: dict[str, Any]) -> bytes:
        """Dump dict."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def loads(cls, var: Union[str, bytes]) -> dict[str, Any]:
        """Load json."""
        raise NotImplementedError
