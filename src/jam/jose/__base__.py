# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from jam.jose.__base_storage__ import BaseStorage


REGISTERED_HEADER_NAMES = frozenset(
    {
        "alg",
        "jku",
        "jwk",
        "kid",
        "x5u",
        "x5c",
        "x5t",
        "x5t#S256",
        "typ",
        "cty",
        "crit",
    }
)

RESERVED_CLAIMS = frozenset({"typ", "cty"})


class BaseJWT(ABC):
    """Base JWT."""

    JWS: type[BaseJWS]

    @abstractmethod
    def encode(
        self,
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
        exp: int | None = None,
        nbf: int | None = None,
        header: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> str:
        """Encode the JWT with the given expire, header, and payload.

        Args:
            exp (int | None): The expiration time in seconds.
            nbf (int | None): The not-before time in seconds.
            iss (str | None): The issuer.
            sub (str | None): The subject.
            aud (str | None): The audience.
            header (dict[str, Any] | None): The header to include in the JWT.
            payload (dict[str, Any] | None): The payload to include in the JWT.

        Returns:
            str: The encoded JWT.
        """
        raise NotImplementedError

    @abstractmethod
    def decode(
        self,
        token: str,
        exp: bool = False,
        nbf: bool = False,
        include_headers: bool = False,
    ) -> dict[str, Any]:
        """Decode the JWT and return the payload.

        Args:
            token (str): The JWT to decode.
            exp (bool): Whether to check the expiration time. Defaults to False.
            nbf (bool): Whether to check the not-before time. Defaults to False.
            include_headers (bool): Whether to include the headers in the result. Defaults to False.

        Returns:
            dict[str, Any]: The decoded payload.
        """
        raise NotImplementedError


class BaseJWS(ABC):
    """Base JSON Web Signature - RFC 7515."""

    @abstractmethod
    def serialize_compact(
        self,
        protected: dict[str, Any],
        payload: bytes | str,
    ) -> str:
        """Create JWS Compact Serialization.

        Args:
            protected (dict[str, Any]): Protected header.
            payload (bytes | str): Payload to sign.

        Returns:
            str: JWS in compact serialization format:
                 BASE64URL(protected).BASE64URL(payload).BASE64URL(signature)
        """
        raise NotImplementedError

    @abstractmethod
    def deserialize_compact(
        self,
        s: str,
        validate: bool = True,
    ) -> dict[str, Any]:
        """Parse JWS Compact Serialization.

        Args:
            s (str): JWS in compact serialization format.
            validate (bool): Whether to validate signature. Defaults to True.

        Returns:
            dict[str, Any]: Parsed JWS with keys:
                - header: Protected header dict
                - payload: Decoded payload (str or dict)
                - signature: Raw signature bytes

        Raises:
            JamJWSVerificationError: If validation fails.
        """
        raise NotImplementedError


class BaseJWK(ABC):
    """Base JWK."""

    __storage: BaseStorage

    @classmethod
    @abstractmethod
    def get(cls, name: str) -> BaseJWK:
        """Get key from storage.

        Args:
            name (str): Key name

        Returns:
            BaseJWK: JSON Web Key
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def store(self) -> None:
        """Store key in storage.

        Args:
            name (str): Key name
            key (BaseJWK): JSON Web Key
        """
        raise NotImplementedError
