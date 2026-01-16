# -*- coding: utf-8 -*-

import datetime
from typing import Literal, Optional, Union

from jam.logger import BaseLogger


try:
    from redis import Redis
except ImportError:
    raise ImportError(
        """
        No required packages found, looks like you didn't install them:
        `pip install "jamlib[redis]"`
        """
    )

from jam.jwt.lists.__abc_list_repo__ import BaseJWTList


class RedisList(BaseJWTList):
    """Black/White lists in Redis, most optimal format.

    Dependency required: `pip install jamlib[redis]`

    Attributes:
        __list__ (Redis): Redis instance
        exp (int | None): Token lifetime
    """

    def __init__(
        self,
        type: Literal["white", "black"],
        redis_uri: Union[str, "Redis"],
        in_list_life_time: Optional[int] = None,
        logger: Optional[BaseLogger] = None,
    ) -> None:
        """Class constructor.

        Args:
            type (Literal["white", "black"]): Type og list
            redis_uri (str): Uri to redis connect
            in_list_life_time (int | None): The lifetime of a token in the list
            logger (Optional[BaseLogger], optional): Logger instance. Defaults to None.
        """
        super().__init__(list_type=type)
        if isinstance(redis_uri, str):
            self.__list__ = Redis.from_url(redis_uri, decode_responses=True)
        else:
            self.__list__ = redis_uri
        self.exp = in_list_life_time
        self._logger = logger

    def add(self, token: str) -> None:
        """Method for adding token to list.

        Args:
            token (str): Your JWT token

        Returns:
            (None)
        """
        self.__list__.set(
            name=token, value=str(datetime.datetime.now()), ex=self.exp
        )
        if self._logger:
            self._logger.info("Set token in list.")
            self._logger.debug(f"Set {token} in list")
        return None

    def check(self, token: str) -> bool:
        """Method for checking if a token is present in the list.

        Args:
            token (str): Your JWT token

        Returns:
            (bool)
        """
        if self._logger:
            self._logger.debug(f"Checking token in {self.__list_type__} list (token length: {len(token)} chars)")
        _token = self.__list__.get(name=token)
        result = bool(_token)
        if self._logger:
            self._logger.debug(f"Token {'found' if result else 'not found'} in {self.__list_type__} list")
        return result

    def delete(self, token: str) -> None:
        """Method for removing a token from a list.

        Args:
            token (str): Your JWT token

        Returns:
            None
        """
        if self._logger:
            self._logger.debug(f"Deleting token from {self.__list_type__} list (token length: {len(token)} chars)")
        deleted_count = self.__list__.delete(token)
        if self._logger:
            self._logger.debug(f"Token removed from {self.__list_type__} list, deleted {deleted_count} key(s)")
        return None
