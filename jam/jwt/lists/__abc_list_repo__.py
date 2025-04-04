# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class AbstracttListRepo(ABC):
    """Abstrac class for lists manipulation."""

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
