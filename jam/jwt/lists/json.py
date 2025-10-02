# -*- coding: utf-8 -*-

import datetime
from typing import Literal

from jam.__logger__ import logger


try:
    from tinydb import Query, TinyDB
except ImportError:
    raise ImportError(
        """
        No required packages found, looks like you didn't install them:
        `pip install "jamlib[json]"`
        """
    )

from jam.jwt.lists.__abc_list_repo__ import BaseJWTList


class JSONList(BaseJWTList):
    """Black/White list in JSON format, not recommended for blacklists  because it is not convenient to control token lifetime.

    Dependency required:
    `pip install jamlib[json]`

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
        logger.info(f"Save JSON to: {json_path}")

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

        logger.info("Set token in list.")
        logger.debug(f"Set {token} in list")
        logger.debug(f"JSON document: {_doc}")
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
