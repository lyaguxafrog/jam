# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from jam.jose.__base_storage__ import BaseStorage


class BaseJWT(ABC):
    """Base JWT."""

    JWS: type[BaseJWS]

    @abstractmethod
    def encode(
        self,
        iss: str | None = None,
        sup: str | None = None,
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
            sup (str | None): The subject.
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
    """Base JSON Web Signature."""

    @abstractmethod
    def sign(self, header: dict[str, Any] | None, data: dict[str, Any]) -> str:
        """Sign the given data and return the JWS.

        Args:
            header (dict[str, Any] | None): The header to include in the JWS.
            data (dict[str, Any]): The data to sign.

        Returns:
            str: The JWS.
        """
        raise NotImplementedError

    @abstractmethod
    def verify(self, jws: str, verify: bool = True) -> dict[str, Any]:
        """Verify the given JWS against the given data.

        Args:
            jws (str): The JWS to verify.
            verify (bool, optional): Whether to verify the JWS. Defaults to True.

        Returns:
            dict[str, Any]: The verified data.

        Raises:
            JamJWSVerificationError: If the JWS verification fails.
        """
        raise NotImplementedError


class BaseJWK(ABC):
    """Base JSON Web Key."""

    storage: BaseStorage

    @abstractmethod
    def construct(self, key_data: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Construct the JWK from the given data.

        Args:
            key_data (dict[str, Any]): The key data to construct the JWK from.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def store(
        cls,
        name: str,
        key: dict[str, Any],
        memory: bool = True,
        store_path: str | None = None,
    ) -> None:
        """Store the JWK in memory or a file.

        Args:
            name (str): The name of the JWK.
            key (dict[str, Any]): The key data to store.
            memory (bool): Whether to store the JWK in memory. Defaults to True.
            store_path (str | None): The path to store the JWK to. Defaults to None.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get(
        cls, name: str, storage: str | None = None
    ) -> dict[str, Any] | None:
        """Get JWK by name from memory or a file.

        Args:
            name (str): The name of the JWK to get.
            storage (str | None): The storage to get the JWK from. Defaults to None.

        Returns:
            dict[str, Any] | None: The JWK data, or None if not found.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def delete(cls, name: str, storage: str | None = None) -> None:
        """Delete JWK by name from memory or a file.

        Args:
            name (str): The name of the JWK to delete.
            storage (str | None): The storage to delete the JWK from. Defaults to None.
        """
        raise NotImplementedError


class BaseJWE(ABC):
    """Base JSON Web Encryption."""

    @abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes:
        """Encrypt the plaintext.

        Args:
            plaintext (bytes): The plaintext to encrypt.

        Returns:
            bytes: The encrypted ciphertext.
        """
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> bytes:
        """Decrypt the ciphertext.

        Args:
            ciphertext (bytes): The ciphertext to decrypt.

        Returns:
            bytes: The decrypted plaintext.
        """
        raise NotImplementedError
