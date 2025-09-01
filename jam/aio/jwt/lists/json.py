# -*- coding: utf-8 -*-

import datetime
from asyncio import to_thread
from typing import Literal

from jam.jwt.lists.__abc_list_repo__ import BaseJWTList


try:
    from tinydb import Query, TinyDB
except ImportError:
    raise ImportError(
        """
        No required packages found, looks like you didn't install them:
        `pip install "jamlib[json-lists]"`
        """
    )


class JSONList(BaseJWTList):
    """Black/White list in JSON format, not recommended for blacklists because it is not convenient to control token lifetime.

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

    async def add(self, token: str) -> None:
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

        await to_thread(self.__list__.insert, _doc)
        return None

    async def check(self, token: str) -> bool:
        """Method for checking if a token is present in list.

        Args:
            token (str): Your jwt token

        Returns:
            (bool)
        """
        cond = Query()
        _token = await to_thread(self.__list__.search, cond.token == token)
        return bool(_token)

    async def delete(self, token: str) -> None:
        """Method for removing token from list.

        Args:
            token (str): Your jwt token

        Returns:
            (None)
        """
        cond = Query()
        await to_thread(self.__list__.remove, cond.token == token)
