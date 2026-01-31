# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any

from jam.jwt.lists import BaseJWTList


class BaseJWT(ABC):
    """Base JWT module."""

    list: BaseJWTList | None = None

    def _list_built(self, list_config: dict[str, Any]) -> BaseJWTList:
        """Builder list."""
        match list_config["backend"]:
            case "redis":
                from jam.jwt.lists.redis import RedisList

                list_config.pop("backend")
                return RedisList(**list_config)
            case "json":
                from jam.jwt.lists.json import JSONList

                list_config.pop("backend")
                return JSONList(**list_config)
            case _:
                raise ValueError(f"Unknown list type: {list_config['type']}")

    @abstractmethod
    def encode(
        self,
        payload: dict[str, Any],
    ) -> str:
        """Encode token.

        Args:
            payload (dict[str, Any]): JWT Payload

        Returns:
            str: JWT
        """
        raise NotImplementedError

    @abstractmethod
    def decode(
        self, token: str, public_key: Any | None = None
    ) -> dict[str, Any]:
        """Decode token.

        Args:
            token (str): JWT
            public_key (Any | None): Decode with public key if needed

        Returns:
            dict: Payload
        """
        raise NotImplementedError
