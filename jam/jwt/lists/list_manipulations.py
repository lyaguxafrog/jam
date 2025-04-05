# -*- coding: utf-8 -*-

import datetime
from typing import Literal

from redis import Redis
from tinydb import Query, TinyDB

from jam.jwt.lists.__abc_list_repo__ import ABCList


class JSONList(ABCList):
    """Black/White list in JSON format, not recommended for blacklists  because it is not convenient to control token lifetime.

    Dependency required:
    `pip install jamlib[json-lists]`

    Attributes:
        __list__ (TinyDB): TinyDB instance

    Methods:
        add: adding token to list
        check: check token in list
        delete: removing token from list
    """

    def __init__(
        self, type: Literal["white", "black"], json_path: str = "whitelist.json"
    ) -> None:
        """Class constructor.

        Args:
            type (Literal["white", "black"]): Type of list
            json_path (str): Path to .json file
        """
        super().__init__(list_type=type)
        self.__list__ = TinyDB(json_path)

    def add(self, token: str) -> None:
        """Method for adding token to list.

        Args:
            token (str): Your JWT token

        Returns:
            (None)
        """
        _doc = {
            "token": token,
            "timestamp": datetime.datetime.now().timestamp(),
        }

        from icecream import ic

        ic(self.__list__.insert(_doc))
        return None

    def check(self, token: str) -> bool:
        """Method for checking if a token is present in list.

        Args:
            token (str): Your jwt token

        Returns:
            (bool)
        """
        cond = Query()
        _token = self.__list__.search(cond.token == token)
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
        self.__list__.remove(cond.token == token)


class RedisList(ABCList):
    """Black/White lists in Redis, most optimal format.

    Dependency required: `pip install jamlib[redis-lists]`

    Attributes:
        __list__ (Redis): Redis instance
        exp (int | None): Token lifetime
    """

    def __init__(
        self,
        type: Literal["white", "black"],
        redis_instance: Redis,
        in_list_life_time: int | None,
    ) -> None:
        """Class constructor.

        Args:
            type (Literal["white", "black"]): Type og list
            redis_instance (Redis): `redis.Redis`
            in_list_life_time (int | None): The lifetime of a token in the list
        """
        super().__init__(list_type=type)
        self.__list__ = redis_instance
        self.exp = in_list_life_time

    def add(self, token: str) -> None:
        """Method for adding token to list.

        Args:
            token (str): Your JWT token

        Returns:
            (None)
        """
        self.__list__.set(name=token, value="", ex=self.exp)
        return None

    def check(self, token: str) -> bool:
        """Method for checking if a token is present in the list.

        Args:
            token (str): Your JWT token

        Returns:
            (bool)
        """
        _token = self.__list__.get(name=token)
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
        self.__list__.delete(token)
        return None
