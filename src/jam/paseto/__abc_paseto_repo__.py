# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Literal, Optional, TypeVar, Union

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from jam.__abc_encoder__ import BaseEncoder
from jam.encoders import JsonEncoder


PASETO = TypeVar("PASETO", bound="BasePASETO")


class BasePASETO(ABC):
    """Base PASETO instance."""

    _VERSION: str

    def __init__(self):
        """Constructor."""
        self._secret: Optional[bytes] = None
        self._purpose: Optional[Literal["local", "public"]] = None

    @property
    def purpose(self) -> Optional[Literal["local", "public"]]:
        """Return PASETO purpose."""
        return self._purpose

    @staticmethod
    def _encrypt(key: bytes, nonce: bytes, data: bytes) -> bytes:
        """Encrypt data using AES-256-CTR."""
        try:
            cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
            return ciphertext
        except Exception as e:
            raise ValueError(f"Failed to encrypt: {e}")

    @staticmethod
    def _decrypt(key: bytes, nonce: bytes, data: bytes) -> bytes:
        """Decrypt data using AES-256-CTR."""
        try:
            cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(data) + decryptor.finalize()
            return plaintext
        except Exception as e:
            raise ValueError(f"Failed to decrypt: {e}")

    @classmethod
    @abstractmethod
    def key(
        cls: type[PASETO],
        purpose: Literal["local", "public"],
        key: Union[str, bytes],
    ) -> PASETO:
        """Create a PASETO instance with the given key.

        Args:
            purpose: 'local' (symmetric encryption) or 'public' (asymmetric signing)
            key: raw bytes or PEM text depending on purpose

        Returns:
            PASETO: configured PASETO instance for encoding/decoding tokens.
        """
        raise NotImplementedError

    @abstractmethod
    def encode(
        self,
        payload: dict[str, Any],
        footer: Optional[Union[dict[str, Any], str]] = None,
        serializer: BaseEncoder = JsonEncoder,
    ) -> str:
        """Generate token from key instance.

        Args:
            payload (dict[str, Any]): Payload for token
            footer (dict[str, Any] | str  | None): Token footer
            serializer (BaseEncoder): JSON Encoder
        """
        raise NotImplementedError

    @abstractmethod
    def decode(
        self,
        token: str,
        serializer: BaseEncoder = JsonEncoder,
    ) -> tuple[dict[str, Any], Optional[dict[str, Any]]]:
        """Decode PASETO.

        Args:
            token (str): Token
            serializer (BaseEncoder): JSON Encoder

        Returns:
            tuple[dict[str, Any], Optional[dict[str, Any]]]: Payload, footer
        """
        raise NotImplementedError
