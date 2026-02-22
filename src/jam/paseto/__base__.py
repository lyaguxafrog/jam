# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Literal, TypeVar

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPublicKey,
)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from jam.__base_encoder__ import BaseEncoder
from jam.encoders import JsonEncoder
from jam.exceptions import JamPASETOInvalidRSAKey


PASETO = TypeVar("PASETO", bound="BasePASETO")
RSAKeyLike = str | bytes | RSAPrivateKey | RSAPublicKey


class BasePASETO(ABC):
    """Base PASETO instance."""

    _VERSION: str

    def __init__(self):
        """Constructor."""
        self._secret: Any | None = None
        self._public_key: RSAPublicKey | None = None
        self._purpose: Literal["local", "public"] | None = None

    @property
    def purpose(self) -> Literal["local", "public"] | None:
        """Return PASETO purpose."""
        return self._purpose

    @staticmethod
    def load_rsa_key(
        key: RSAKeyLike | None, *, private: bool = True
    ) -> RSAPrivateKey | RSAPublicKey | None:
        """Load rsa key from string | bytes.

        Args:
            key (RSAKeyLike | None): RSA Key
            private (bool): Private or public

        Raises:
            JamPASETOInvalidRSAKey: Invalid RSA key format.
        """
        if key is None:
            return None
        if isinstance(key, (RSAPublicKey | RSAPrivateKey)):
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
                raise JamPASETOInvalidRSAKey(
                    message=f"Invalid RSA {'private' if private else 'public'} key format.",
                    details={"error": str(e)}
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
        key: str | bytes,
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
        footer: dict[str, Any] | str | None = None,
        serializer: type[BaseEncoder] | BaseEncoder = JsonEncoder,
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
        serializer: type[BaseEncoder] | BaseEncoder = JsonEncoder,
    ) -> tuple[dict[str, Any], dict[str, Any] | None]:
        """Decode PASETO.

        Args:
            token (str): Token
            serializer (BaseEncoder): JSON Encoder

        Returns:
            tuple[dict[str, Any], Optional[dict[str, Any]]]: Payload, footer
        """
        raise NotImplementedError
