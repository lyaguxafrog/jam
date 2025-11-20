# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseJWT(ABC):
    """Base JWT module."""

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
        self, token: str, public_key: Optional[Any] = None
    ) -> dict[str, Any]:
        """Decode token.

        Args:
            token (str): JWT
            public_key (Any | None): Decode with public key if needed

        Returns:
            dict: Payload
        """
        raise NotImplementedError
