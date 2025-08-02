# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Literal, Protocol


class ABCList(ABC):
    """Abstract class for lists manipulation."""

    def __init__(self, list_type: Literal["white", "black"]) -> None:
        """Class constructor."""
        self.__list_type__ = list_type

    @abstractmethod
    async def add(self, token: str) -> None:
        """Method for adding token to list."""
        raise NotImplementedError

    @abstractmethod
    async def check(self, token: str) -> bool:
        """Method for checking if a token is present in the list."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, token: str) -> None:
        """Method for removing a token from a list."""
        raise NotImplementedError


class JWTList(Protocol):
    """Protocol class for lists."""

    __list_type__: Literal["black", "white"]

    async def add(self, token: str) -> None:
        """Method for adding token to list."""
        pass

    async def check(self, token: str) -> bool:
        """Method for checking if a token is present in the list."""
        pass

    async def delete(self, token: str) -> None:
        """Method for removing a token from a list."""
        pass
