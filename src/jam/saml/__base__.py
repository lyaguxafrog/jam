# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseSAML(ABC):
    """SAML tokens module."""

    @abstractmethod
    def encode(
        self,
        *,
        subject: str,
        audience: str,
        issuer: str,
        attributes: dict[str, Any],
        expiration_seconds: int | None = 300,
    ) -> str:
        """Generate a SAML token.

        Args:
            subject (str): The subject of the token.
            audience (str): The audience of the token.
            issuer (str): The issuer of the token.
            attributes (dict[str, Any]): The attributes of the token.
            expiration_seconds (int | None): The expiration time of the token in seconds.

        Returns:
            The SAML token as a string.
        """
        raise NotImplementedError

    @abstractmethod
    def decode(
        self,
        token: str,
    ) -> dict[str, Any]:
        """Decode a SAML token.

        Args:
            token (str): The SAML token to decode.

        Returns:
            The decoded token as a dictionary.
        """
        raise NotImplementedError
