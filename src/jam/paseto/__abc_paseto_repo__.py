# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Literal, Optional, TypeVar, Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPublicKey,
)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from jam.__abc_encoder__ import BaseEncoder
from jam.encoders import JsonEncoder


PASETO = TypeVar("PASETO", bound="BasePASETO")
RSAKeyLike = Union[str, bytes, RSAPrivateKey, RSAPublicKey]


class BasePASETO(ABC):
    """Base PASETO instance."""

    _VERSION: str

    def __init__(self):
        """Constructor."""
        self._secret: Optional[Any] = None
        self._public_key: Optional[RSAPublicKey] = None
        self._purpose: Optional[Literal["local", "public"]] = None

    @property
    def purpose(self) -> Optional[Literal["local", "public"]]:
        """Return PASETO purpose."""
        return self._purpose

    @staticmethod
    def load_rsa_key(
        key: Optional[RSAKeyLike], *, private: bool = True
    ) -> Union[RSAPrivateKey, RSAPublicKey, None]:
        """Load rsa key from string | bytes.

        Args:
            key (RSAKeyLike | None): RSA Key
            private (bool): Private or public
        """
        if key is None:
            return None
        if isinstance(key, (RSAPublicKey, RSAPrivateKey)):
            return key
        if isinstance(key, str):
            key = key.encode("utf-8")
        try:
            if private:
                return serialization.load_pem_private_key(key, password=None)
            else:
                return serialization.load_pem_public_key(key)
        except ValueError:
            try:
                if private:
                    return serialization.load_der_private_key(
                        key, password=None
                    )
                else:
                    return serialization.load_der_public_key(key)
            except Exception as e:
                raise ValueError(
                    f"Invalid RSA {'private' if private else 'public'} key format: {e}"
                )

    @staticmethod
    def _rsa_pem_check(key: RSAKeyLike) -> bool:
        if isinstance(key, str):
            if key.startswith("-----BEGIN PRIVATE"):
                return True
            elif key.startswith("-----BEGIN RSA PRIVATE"):
                return True
            elif key.startswith("-----BEGIN EC PRIVATE"):
                return True
        elif isinstance(key, bytes):
            if key.startswith(b"-----BEGIN PRIVATE"):
                return True
            elif key.startswith(b"-----BEGIN RSA PRIVATE"):
                return True
            elif key.startswith(b"-----BEGIN EC PRIVATE"):
                return True
        elif isinstance(key, RSAPrivateKey):
            return True
        return False

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
