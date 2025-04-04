# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from redis import Redis
from tinydb import Query, TinyDB


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


# TODO: Made with aiotinydb too
class JSONList(AbstracttListRepo):
    """Black/White list in JSON format, not recommended for blacklists  because it is not convenient to control token lifetime.

    Dependency required:
    `pip install jamlib[json-list]`

    Attributes:
        list (TinyDB): TinyDB instance

    Methods:
        add: adding token to list
        check: check token in list
        delete: removing token from list
        all: return all tokens in list
    """

    def __init__(self, json_path: str = "whitelist.json") -> None:
        """Class constructor.

        Args:
            json_path (str): Path to .json file
        """
        self.list = TinyDB(json_path)

    def add(self, token: str) -> None:
        """Method for adding token to list.

        Args:
            token (str): Your JWT token

        Returns:
            (None)
        """
        _doc = {"token": token}

        self.list.insert(_doc)
        return None

    def check(self, token: str) -> bool:
        """Method for checking if a token is present in list.

        Args:
            token (str): Your jwt token

        Returns:
            (bool)
        """
        cond = Query()
        _token = self.list.search(cond.token == token)
        if _token:
            return True
        else:
            return False

    def delete(self, token: str) -> None:
        """Method for removing token from list.

        Args:
            token (str): Your jwt token

        Returns:
            (None)
        """
        cond = Query()
        self.list.remove(cond.token == token)

    def all(self) -> list:
        """Returns a list of all tokens in the list.

        Args:
            (list)
        """
        return self.list.all()


class RedisList(AbstracttListRepo):
    """Black/White lists in Redis, most optimal format."""

    def __init__(
        self, redis_instance: Redis, in_list_life_time: int | None
    ) -> None:
        """Class constructor.

        Args:
            redis_instance (Redis): `redis.Redis`
            in_list_life_time (int | None): The lifetime of a token in the list
        """
        self.list = redis_instance
        self.exp = in_list_life_time

    def add(self, token: str) -> None:
        """Method for adding token to list.

        Args:
            token (str): Your JWT token

        Returns:
            (None)
        """
        self.list.set(name=token, ex=self.exp)
        return None

    def check(self, token: str) -> bool:
        """Method for checking if a token is present in the list.

        Args:
            token (str): Your JWT token

        Returns:
            (bool)
        """
        _token = self.list.get(name=token)
        if not _token:
            return False
        else:
            return True

    def delete(self, token: str) -> None:
        """Method for removing a token from a list.

        Args:
            token (str): Your JWT token

        Returns:
            None
        """
        self.list.delete(token)
        return None
