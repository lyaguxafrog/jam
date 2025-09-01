# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Literal


class BaseJWTList(ABC):
    """Abstract class for lists manipulation."""

    def __init__(self, list_type: Literal["white", "black"]) -> None:
        """Class constructor."""
        self.__list_type__ = list_type

    @abstractmethod
    def add(self, token: str) -> Any:
        """Method for adding token to list."""
        raise NotImplementedError

    @abstractmethod
    def check(self, token: str) -> Any:
        """Method for checking if a token is present in the list."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, token: str) -> Any:
        """Method for removing a token from a list."""
        raise NotImplementedError
