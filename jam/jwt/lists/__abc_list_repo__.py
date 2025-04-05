# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Literal, Protocol


class ABCList(ABC):
    """Abstrac class for lists manipulation."""

    def __init__(self, list_type: Literal["white", "black"]) -> None:
        """Class constructor."""
        self.__list_type__ = list_type

    @abstractmethod
    def add(self, token: str) -> None:
        """Method for adding token to list."""
        raise NotImplementedError

    @abstractmethod
    def check(self, token: str) -> bool:
        """Method for checking if a token is present in the list."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, token: str) -> None:
        """Method for removing a token from a list."""
        raise NotImplementedError


class JWTList(Protocol):
    """Protocol class for lists."""

    __list_type__: Literal["black", "white"]

    def add(self, token: str) -> None:
        """Method for adding token to list."""
        pass

    def check(self, token: str) -> bool:
        """Method for checking if a token is present in the list."""
        pass

    def delete(self, token: str) -> None:
        """Method for removing a token from a list."""
        pass
