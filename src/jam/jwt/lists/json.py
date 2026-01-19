# -*- coding: utf-8 -*-

import datetime
from typing import Literal

from jam.logger import BaseLogger


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
        self,
        type: Literal["white", "black"],
        json_path: str = "whitelist.json",
        logger: BaseLogger | None = None,
    ) -> None:
        """Class constructor.

        Args:
            type (Literal["white", "black"]): Type of list
            json_path (str): Path to .json file
            logger (Optional[BaseLogger], optional): Logger instance. Defaults to None.
        """
        super().__init__(list_type=type)
        self.__list__ = TinyDB(json_path)
        self._logger = logger
        if self._logger:
            self._logger.info(f"Save JSON to: {json_path}")

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

        if self._logger:
            self._logger.info("Set token in list.")
            self._logger.debug(f"Set {token} in list")
            self._logger.debug(f"JSON document: {_doc}")
        return None

    def check(self, token: str) -> bool:
        """Method for checking if a token is present in list.

        Args:
            token (str): Your jwt token

        Returns:
            (bool)
        """
        if self._logger:
            self._logger.debug(
                f"Checking token in {self.__list_type__} list (token length: {len(token)} chars)"
            )
        cond = Query()
        _token = self.__list__.search(cond.token == token)
        result = bool(_token)
        if self._logger:
            self._logger.debug(
                f"Token {'found' if result else 'not found'} in {self.__list_type__} list"
            )
        return result

    def delete(self, token: str) -> None:
        """Method for removing token from list.

        Args:
            token (str): Your jwt token

        Returns:
            (None)
        """
        if self._logger:
            self._logger.debug(
                f"Deleting token from {self.__list_type__} list (token length: {len(token)} chars)"
            )
        cond = Query()
        removed_count = self.__list__.remove(cond.token == token)
        if self._logger:
            self._logger.debug(
                f"Token removed from {self.__list_type__} list, deleted {len(removed_count)} document(s)"
            )
