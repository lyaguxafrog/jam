# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any


class BaseStorage(ABC):
    """Base class for storage backends."""

    @abstractmethod
    def get(cls, name: str) -> dict[str, Any] | None:
        """Get a key by name.

        Args:
            name (str): The name of the key to retrieve.
        """
        raise NotImplementedError

    @abstractmethod
    def store(cls, name: str, data: dict[str, Any]) -> None:
        """Store a key with the given name and data.

        Args:
            name (str): The name of the key to store.
            data (dict[str, Any]): The data to store.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(cls, name: str) -> None:
        """Delete a key by name.

        Args:
            name (str): The name of the key to delete.
        """
        raise NotImplementedError
