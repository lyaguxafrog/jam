# -*- coding: utf-8 -*-
import datetime

from motor import MotorClient
from redis import Redis
from tinydb import Query, TinyDB

from jam.jwt.lists.__abc_list_repo__ import AbstracttListRepo


class JSONList(AbstracttListRepo):
    """Black/White list in JSON format, not recommended for blacklists  because it is not convenient to control token lifetime.

    Dependency required:
    `pip install jamlib[json-list]`

    Attributes:
        __list__ (TinyDB): TinyDB instance

    Methods:
        add: adding token to list
        check: check token in list
        delete: removing token from list
    """

    def __init__(self, json_path: str = "whitelist.json") -> None:
        """Class constructor.

        Args:
            json_path (str): Path to .json file
        """
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

        self.__list__.insert(_doc)
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
        self.__list__ = redis_instance
        self.exp = in_list_life_time

    def add(self, token: str) -> None:
        """Method for adding token to list.

        Args:
            token (str): Your JWT token

        Returns:
            (None)
        """
        self.__list__.set(name=token, ex=self.exp)
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


class MongoList(AbstracttListRepo):
    """Black/White lists in MongoDB."""

    def __init__(
        self, mongo_str: str, db_name: str, collection_name: str = "jam_list"
    ) -> None:
        """Class constructor.

        Args:
            mongo_str (str): MongoDB connection string
            db_name (str): MongoDB DB Name
            collection_name (str): Collection name, by default "jam_list"
        """
        self._client = MotorClient(mongo_str)
        self._db = self._client[db_name]
        self.__list__ = self._db[collection_name]

    def add(self, token: str) -> None:
        """Method for adding token to list.

        Args:
            token (str): Your jwt token

        Returns:
            (None)
        """
        document = {
            "token": token,
            "timestamp": datetime.datetime.now().timestamp(),
        }

        self.__list__.insert_one(document=document)
        return None

    def check(self, token: str) -> bool:
        """Method for checking if a token is present in the list.

        Args:
            token (str): Your jwt token

        Returns:
            (bool)
        """
        _token = self.__list__.find_one(token=token)
        if _token:
            return True
        else:
            return False

    def delete(self, token: str) -> None:
        """Method for removing a token from a list.

        Args:
            token (str): Your jwt token
        """
        self.__list__.delete_one({"token": token})
        return None
