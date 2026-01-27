# -*- coding: utf-8 -*-

# Apache License
# Version 2.0, January 2004
# http://www.apache.org/licenses/
#
# Copyright 2025 Adrian Makridenko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from abc import ABC, abstractmethod
import hashlib
import hmac
from typing import Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)

from jam.jwt.__types__ import KeyLike
from jam.jwt.utils import base64url_encode
from jam.logger import BaseLogger


class BaseAlgorithm(ABC):
    """Base class for JWT signing algorithms."""

    def __init__(
        self,
        alg: str,
        secret: KeyLike,
        password: bytes | None,
        logger: BaseLogger,
    ) -> None:
        """Initialize algorithm.

        Args:
            alg (str): Algorithm name
            secret (KeyLike): Secret key
            password (bytes | None): Password for private key
            logger (BaseLogger): Logger instance
        """
        self.alg = alg
        self._secret = secret
        self._password = password
        self._logger = logger

    @abstractmethod
    def sign(self, data: bytes) -> str:
        """Sign data.

        Args:
            data (bytes): Data to sign

        Returns:
            str: Base64url encoded signature
        """
        raise NotImplementedError

    @abstractmethod
    def verify(self, sig: bytes, data: bytes, key: KeyLike) -> None:
        """Verify signature.

        Args:
            sig (bytes): Signature to verify
            data (bytes): Data that was signed
            key (KeyLike): Key for verification

        Raises:
            ValueError: If signature is invalid
        """
        raise NotImplementedError

    def _load_key_data(self, data: str | bytes) -> bytes:
        """Load key data from string or bytes.

        Args:
            data (str | bytes): Key data or path to key file

        Returns:
            bytes: Key bytes
        """
        if isinstance(data, bytes):
            return data
        from pathlib import Path

        path = Path(data)
        return path.read_bytes() if path.is_file() else data.encode()

    def _load_private_key(
        self, key_bytes: bytes | None, key_obj: Any | None
    ) -> Any:
        """Load private key from bytes or use key object.

        Args:
            key_bytes (bytes | None): Key bytes
            key_obj (Any | None): Key object

        Returns:
            Any: Private key object

        Raises:
            ValueError: If key cannot be loaded
        """
        if key_bytes is None:
            return key_obj

        try:
            return serialization.load_pem_private_key(
                key_bytes, password=self._password
            )
        except ValueError as e:
            self._logger.error(
                f"Failed to load private key: {e}",
                exc_info=True,
            )
            raise ValueError(f"Invalid private key format: {e}") from e

    def _load_public_key_auto(self, key: KeyLike) -> Any:
        """Load public key automatically from various formats.

        Args:
            key (KeyLike): Key in various formats

        Returns:
            Any: Public key object

        Raises:
            ValueError: If key cannot be loaded
        """
        if hasattr(key, "public_key"):
            return key.public_key()

        key_bytes = (
            self._load_key_data(key) if isinstance(key, (str, bytes)) else None
        )
        if not key_bytes:
            return key

        try:
            return serialization.load_pem_public_key(key_bytes)
        except ValueError:
            try:
                priv = serialization.load_pem_private_key(
                    key_bytes, password=self._password
                )
                self._logger.debug(
                    "Extracted public key from private PEM automatically."
                )
                return priv.public_key()
            except ValueError as e:
                self._logger.error(
                    f"Failed to load public key: {e}",
                    exc_info=True,
                )
                raise ValueError(f"Invalid key format: {e}") from e


class HSAlgorithm(BaseAlgorithm):
    """HMAC-based algorithms (HS256, HS384, HS512)."""

    def sign(self, data: bytes) -> str:
        """Sign data using HMAC.

        Args:
            data (bytes): Data to sign

        Returns:
            str: Base64url encoded signature
        """
        self._logger.debug(f"Signing with {self.alg}")
        key = (
            self._secret.encode()
            if isinstance(self._secret, str)
            else self._secret
        )
        if not isinstance(key, bytes):
            raise ValueError(
                f"Invalid key type for {self.alg}: expected str or bytes"
            )

        digest = getattr(hashlib, f"sha{self.alg[2:]}")
        sig = hmac.new(key, data, digest).digest()
        return base64url_encode(sig)

    def verify(self, sig: bytes, data: bytes, key: KeyLike) -> None:
        """Verify HMAC signature.

        Args:
            sig (bytes): Signature to verify
            data (bytes): Data that was signed
            key (KeyLike): Key for verification

        Raises:
            ValueError: If signature is invalid
        """
        self._logger.debug(f"Verifying {self.alg} signature")
        k = key.encode() if isinstance(key, str) else key
        if not isinstance(k, bytes):
            raise ValueError(
                f"Invalid key type for {self.alg}: expected str or bytes"
            )

        digest = getattr(hashlib, f"sha{self.alg[2:]}")
        expected = hmac.new(k, data, digest).digest()
        if not hmac.compare_digest(sig, expected):
            self._logger.warning("HMAC signature verification failed")
            raise ValueError("Invalid HMAC signature")


class RSAlgorithm(BaseAlgorithm):
    """RSA PKCS1v15 algorithms (RS256, RS384, RS512)."""

    def _get_private_key(self) -> Any:
        """Get private key for signing.

        Returns:
            Any: Private key object

        Raises:
            ValueError: If key cannot be loaded
        """
        key_bytes = (
            self._load_key_data(self._secret)
            if isinstance(self._secret, (str, bytes))
            else None
        )
        return self._load_private_key(key_bytes, self._secret)

    def sign(self, data: bytes) -> str:
        """Sign data using RSA PKCS1v15.

        Args:
            data (bytes): Data to sign

        Returns:
            str: Base64url encoded signature
        """
        self._logger.debug(f"Signing with {self.alg}")
        try:
            private_key = self._get_private_key()
            hash_alg = getattr(hashes, f"SHA{self.alg[2:]}")()
            sig = private_key.sign(data, padding.PKCS1v15(), hash_alg)
            return base64url_encode(sig)
        except Exception as e:
            self._logger.error(
                f"Failed to sign with {self.alg}: {e}",
                exc_info=True,
            )
            raise ValueError(f"Signing failed: {e}") from e

    def verify(self, sig: bytes, data: bytes, key: KeyLike) -> None:
        """Verify RSA PKCS1v15 signature.

        Args:
            sig (bytes): Signature to verify
            data (bytes): Data that was signed
            key (KeyLike): Key for verification

        Raises:
            ValueError: If signature is invalid
        """
        self._logger.debug(f"Verifying {self.alg} signature")
        try:
            pub_key = self._load_public_key_auto(key)
            hash_alg = getattr(hashes, f"SHA{self.alg[2:]}")()
            pub_key.verify(sig, data, padding.PKCS1v15(), hash_alg)
        except Exception as e:
            self._logger.warning(
                f"RSA signature verification failed: {e}",
                exc_info=True,
            )
            raise ValueError(f"Invalid RSA signature: {e}") from e


class ESAlgorithm(BaseAlgorithm):
    """ECDSA algorithms (ES256, ES384, ES512)."""

    _CURVE_MAP = {
        "ES256": (ec.SECP256R1(), hashes.SHA256()),
        "ES384": (ec.SECP384R1(), hashes.SHA384()),
        "ES512": (ec.SECP521R1(), hashes.SHA512()),
    }

    def _get_private_key(self) -> Any:
        """Get private key for signing.

        Returns:
            Any: Private key object

        Raises:
            ValueError: If key cannot be loaded
        """
        key_bytes = (
            self._load_key_data(self._secret)
            if isinstance(self._secret, (str, bytes))
            else None
        )
        return self._load_private_key(key_bytes, self._secret)

    def sign(self, data: bytes) -> str:
        """Sign data using ECDSA.

        Args:
            data (bytes): Data to sign

        Returns:
            str: Base64url encoded signature
        """
        self._logger.debug(f"Signing with {self.alg}")
        try:
            private_key = self._get_private_key()
            _, hash_alg = self._CURVE_MAP[self.alg]
            der = private_key.sign(data, ec.ECDSA(hash_alg))
            r, s = decode_dss_signature(der)
            n = (private_key.curve.key_size + 7) // 8
            raw = r.to_bytes(n, "big") + s.to_bytes(n, "big")
            return base64url_encode(raw)
        except Exception as e:
            self._logger.error(
                f"Failed to sign with {self.alg}: {e}",
                exc_info=True,
            )
            raise ValueError(f"Signing failed: {e}") from e

    def verify(self, sig: bytes, data: bytes, key: KeyLike) -> None:
        """Verify ECDSA signature.

        Args:
            sig (bytes): Signature to verify
            data (bytes): Data that was signed
            key (KeyLike): Key for verification

        Raises:
            ValueError: If signature is invalid
        """
        self._logger.debug(f"Verifying {self.alg} signature")
        try:
            pub_key = self._load_public_key_auto(key)
            _, hash_alg = self._CURVE_MAP[self.alg]
            n = (pub_key.curve.key_size + 7) // 8
            if len(sig) != 2 * n:
                raise ValueError(
                    f"Invalid signature length: expected {2 * n}, got {len(sig)}"
                )
            r, s = (
                int.from_bytes(sig[:n], "big"),
                int.from_bytes(sig[n:], "big"),
            )
            der = encode_dss_signature(r, s)
            pub_key.verify(der, data, ec.ECDSA(hash_alg))
        except Exception as e:
            self._logger.warning(
                f"ECDSA signature verification failed: {e}",
                exc_info=True,
            )
            raise ValueError(f"Invalid ECDSA signature: {e}") from e


class PSAlgorithm(BaseAlgorithm):
    """RSA PSS algorithms (PS256, PS384, PS512)."""

    def _get_private_key(self) -> Any:
        """Get private key for signing.

        Returns:
            Any: Private key object

        Raises:
            ValueError: If key cannot be loaded
        """
        key_bytes = (
            self._load_key_data(self._secret)
            if isinstance(self._secret, (str, bytes))
            else None
        )
        return self._load_private_key(key_bytes, self._secret)

    def sign(self, data: bytes) -> str:
        """Sign data using RSA PSS.

        Args:
            data (bytes): Data to sign

        Returns:
            str: Base64url encoded signature
        """
        self._logger.debug(f"Signing with {self.alg}")
        try:
            private_key = self._get_private_key()
            hash_alg = getattr(hashes, f"SHA{self.alg[2:]}")()
            sig = private_key.sign(
                data,
                padding.PSS(
                    mgf=padding.MGF1(hash_alg),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hash_alg,
            )
            return base64url_encode(sig)
        except Exception as e:
            self._logger.error(
                f"Failed to sign with {self.alg}: {e}",
                exc_info=True,
            )
            raise ValueError(f"Signing failed: {e}") from e

    def verify(self, sig: bytes, data: bytes, key: KeyLike) -> None:
        """Verify RSA PSS signature.

        Args:
            sig (bytes): Signature to verify
            data (bytes): Data that was signed
            key (KeyLike): Key for verification

        Raises:
            ValueError: If signature is invalid
        """
        self._logger.debug(f"Verifying {self.alg} signature")
        try:
            pub_key = self._load_public_key_auto(key)
            hash_alg = getattr(hashes, f"SHA{self.alg[2:]}")()
            pub_key.verify(
                sig,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hash_alg),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hash_alg,
            )
        except Exception as e:
            self._logger.warning(
                f"RSA PSS signature verification failed: {e}",
                exc_info=True,
            )
            raise ValueError(f"Invalid RSA PSS signature: {e}") from e


def create_algorithm(
    alg: str,
    secret: KeyLike,
    password: bytes | None,
    logger: BaseLogger,
) -> BaseAlgorithm:
    """Create algorithm instance based on algorithm name.

    Args:
        alg (str): Algorithm name
        secret (KeyLike): Secret key
        password (bytes | None): Password for private key
        logger (BaseLogger): Logger instance

    Returns:
        BaseAlgorithm: Algorithm instance

    Raises:
        ValueError: If algorithm is not supported
    """
    if alg.startswith("HS"):
        return HSAlgorithm(alg, secret, password, logger)
    if alg.startswith("RS"):
        return RSAlgorithm(alg, secret, password, logger)
    if alg.startswith("ES"):
        return ESAlgorithm(alg, secret, password, logger)
    if alg.startswith("PS"):
        return PSAlgorithm(alg, secret, password, logger)

    raise ValueError(f"Unsupported algorithm: {alg}")
