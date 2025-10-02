# -*- coding: utf-8 -*-

import datetime
from typing import Literal, Optional, Union

from jam.jwt.lists.__abc_list_repo__ import BaseJWTList


try:
    from redis.asyncio import Redis
except ImportError:
    raise ImportError(
        """
        No required packages found, looks like you didn't install them:
        `pip install "jamlib[redis]"`
        """
    )


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
        redis_uri: Union[str, Redis],
        in_list_life_time: Optional[int] = None,
    ) -> None:
        """Class constructor.

        Args:
            type (Literal["white", "black"]): Type of list
            redis_uri (str): Uri to redis connect
            in_list_life_time (int | None): The lifetime of a token in the list
        """
        super().__init__(list_type=type)
        if isinstance(redis_uri, str):
            self.__list__ = Redis.from_url(redis_uri, decode_responses=True)
        else:
            self.__list__ = redis_uri
        self.exp = in_list_life_time

    async def add(self, token: str) -> None:
        """Method for adding token to list.

        Args:
            token (str): Your JWT token

        Returns:
            (None)
        """
        await self.__list__.set(
            name=token, value=str(datetime.datetime.now()), ex=self.exp
        )
        return None

    async def check(self, token: str) -> bool:
        """Method for checking if a token is present in the list.

        Args:
            token (str): Your JWT token

        Returns:
            (bool)
        """
        _token = await self.__list__.get(name=token)
        if _token:
            return True
        return False

    async def delete(self, token: str) -> None:
        """Method for removing a token from a list.

        Args:
            token (str): Your JWT token

        Returns:
            None
        """
        await self.__list__.delete(token)
        return None
