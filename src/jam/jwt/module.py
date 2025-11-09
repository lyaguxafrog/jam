# -*- coding: utf-8 -*-

from __future__ import annotations

import hashlib
import hmac
from pathlib import Path
from typing import Any, Literal, Optional, Union

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)

from jam.encoders import BaseEncoder, JsonEncoder
from jam.jwt.__base__ import BaseJWT
from jam.jwt.utils import base64url_decode, base64url_encode
from jam.logger import BaseLogger, logger


KeyLike = Union[
    str,
    bytes,
    rsa.RSAPrivateKey,
    rsa.RSAPublicKey,
    ec.EllipticCurvePrivateKey,
    ec.EllipticCurvePublicKey,
]


class JWT(BaseJWT):
    """JWT factory."""

    def __init__(
        self,
        alg: Literal[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
            "PS256",
            "PS384",
            "PS512",
        ],
        secret: KeyLike,
        password: Optional[Union[str, bytes]] = None,
        serializer: Union[BaseEncoder, type[BaseEncoder]] = JsonEncoder,
        logger: BaseLogger = logger,
    ) -> None:
        """Initalization.

        Args:
            alg (str): JWT Alg
            secret (KeyLike): Secret key
            password (str  | bytes | None): Password for private key
            serializer (BaseEncoder | type[BaseEncoder]): JSON Encoder
            logger (BaseLogger): Logger instance
        """
        self.alg = alg
        self._secret = secret
        self._password = password
        self._logger = logger
        self._serializer = (
            serializer() if isinstance(serializer, type) else serializer
        )

    def _load_key_data(self, data: Union[str, bytes]) -> bytes:
        if isinstance(data, bytes):
            return data
        path = Path(data)
        return path.read_bytes() if path.is_file() else data.encode()

    def _load_public_key_auto(self, key: KeyLike) -> Any:
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
            priv = serialization.load_pem_private_key(
                key_bytes,
                password=(
                    self._password.encode()
                    if isinstance(self._password, str)
                    else self._password
                ),
            )
            self._logger.debug(
                "Extracted public key from private PEM automatically."
            )
            return priv.public_key()

    def _sign_hs(self, data: bytes) -> str:
        key = (
            self._secret.encode()
            if isinstance(self._secret, str)
            else self._secret
        )
        digest = getattr(hashlib, f"sha{self.alg[2:]}")
        sig = hmac.new(key, data, digest).digest()
        return base64url_encode(sig)

    def _sign_rs(self, data: bytes) -> str:
        key_bytes = (
            self._load_key_data(self._secret)
            if isinstance(self._secret, (str, bytes))
            else None
        )
        private_key = (
            serialization.load_pem_private_key(
                key_bytes,
                password=(
                    self._password.encode()
                    if isinstance(self._password, str)
                    else self._password
                ),
            )
            if key_bytes
            else self._secret
        )
        hash_alg = getattr(hashes, f"SHA{self.alg[2:]}")()
        sig = private_key.sign(data, padding.PKCS1v15(), hash_alg)
        return base64url_encode(sig)

    def _sign_es(self, data: bytes) -> str:
        curve_map = {
            "ES256": (ec.SECP256R1(), hashes.SHA256()),
            "ES384": (ec.SECP384R1(), hashes.SHA384()),
            "ES512": (ec.SECP521R1(), hashes.SHA512()),
        }
        _, hash_alg = curve_map[self.alg]
        key_bytes = (
            self._load_key_data(self._secret)
            if isinstance(self._secret, (str, bytes))
            else None
        )
        private_key = (
            serialization.load_pem_private_key(
                key_bytes,
                password=(
                    self._password.encode()
                    if isinstance(self._password, str)
                    else self._password
                ),
            )
            if key_bytes
            else self._secret
        )
        der = private_key.sign(data, ec.ECDSA(hash_alg))
        r, s = decode_dss_signature(der)
        n = (private_key.curve.key_size + 7) // 8
        raw = r.to_bytes(n, "big") + s.to_bytes(n, "big")
        return base64url_encode(raw)

    def _sign_ps(self, data: bytes) -> str:
        key_bytes = (
            self._load_key_data(self._secret)
            if isinstance(self._secret, (str, bytes))
            else None
        )
        private_key = (
            serialization.load_pem_private_key(
                key_bytes,
                password=(
                    self._password.encode()
                    if isinstance(self._password, str)
                    else self._password
                ),
            )
            if key_bytes
            else self._secret
        )
        hash_alg = getattr(hashes, f"SHA{self.alg[2:]}")()
        sig = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hash_alg), salt_length=padding.PSS.MAX_LENGTH
            ),
            hash_alg,
        )
        return base64url_encode(sig)

    def __sign(self, data: bytes) -> str:
        if self.alg.startswith("HS"):
            return self._sign_hs(data)
        if self.alg.startswith("RS"):
            return self._sign_rs(data)
        if self.alg.startswith("ES"):
            return self._sign_es(data)
        if self.alg.startswith("PS"):
            return self._sign_ps(data)
        raise ValueError(f"Unsupported algorithm: {self.alg}")

    def encode(self, payload: dict[str, Any]) -> str:
        """Encode token.

        Args:
            payload (dict[str, Any]): Payload

        Returns:
            str: New token
        """
        header = {"typ": "jwt", "alg": self.alg}
        header_b64 = base64url_encode(self._serializer.dumps(header))
        payload_b64 = base64url_encode(self._serializer.dumps(payload))
        signature = self.__sign(f"{header_b64}.{payload_b64}".encode())
        return f"{header_b64}.{payload_b64}.{signature}"

    def decode(
        self, token: str, public_key: Optional[KeyLike] = None
    ) -> dict[str, Any]:
        """Decode token.

        Args:
            token (str): Token
            public_key (KeyLike | None): Public key

        Raises:
            ValueError: If invalid token

        Returns:
            dict: Payload
        """
        try:
            h_b64, p_b64, s_b64 = token.split(".")
        except ValueError:
            raise ValueError(
                "Invalid token format. Expected header.payload.signature"
            )

        header = self._serializer.loads(base64url_decode(h_b64))
        payload = self._serializer.loads(base64url_decode(p_b64))
        data = f"{h_b64}.{p_b64}".encode()
        sig = base64url_decode(s_b64)

        if header.get("alg") != self.alg:
            raise ValueError(
                f"Algorithm mismatch: expected {self.alg}, got {header.get('alg')}"
            )

        key = public_key or self._secret
        if not self.alg.startswith("HS"):
            key = self._load_public_key_auto(key)

        if self.alg.startswith("HS"):
            self._verify_hs(sig, data, key)
        elif self.alg.startswith("RS"):
            self._verify_rs(sig, data, key)
        elif self.alg.startswith("ES"):
            self._verify_es(sig, data, key)
        elif self.alg.startswith("PS"):
            self._verify_ps(sig, data, key)
        else:
            raise ValueError(f"Unsupported algorithm: {self.alg}")

        return payload

    def _verify_hs(self, sig: bytes, data: bytes, key: KeyLike) -> None:
        k = key.encode() if isinstance(key, str) else key
        digest = getattr(hashlib, f"sha{self.alg[2:]}")
        expected = hmac.new(k, data, digest).digest()
        if not hmac.compare_digest(sig, expected):
            raise ValueError("Invalid HMAC signature")

    def _verify_rs(self, sig: bytes, data: bytes, key: KeyLike) -> None:
        pub_key = self._load_public_key_auto(key)
        hash_alg = getattr(hashes, f"SHA{self.alg[2:]}")()
        pub_key.verify(sig, data, padding.PKCS1v15(), hash_alg)

    def _verify_es(self, sig: bytes, data: bytes, key: KeyLike) -> None:
        pub_key = self._load_public_key_auto(key)
        curve_map = {
            "ES256": (ec.SECP256R1(), hashes.SHA256()),
            "ES384": (ec.SECP384R1(), hashes.SHA384()),
            "ES512": (ec.SECP521R1(), hashes.SHA512()),
        }
        _, hash_alg = curve_map[self.alg]
        n = (pub_key.curve.key_size + 7) // 8
        r, s = int.from_bytes(sig[:n], "big"), int.from_bytes(sig[n:], "big")
        der = encode_dss_signature(r, s)
        pub_key.verify(der, data, ec.ECDSA(hash_alg))

    def _verify_ps(self, sig: bytes, data: bytes, key: KeyLike) -> None:
        pub_key = self._load_public_key_auto(key)
        hash_alg = getattr(hashes, f"SHA{self.alg[2:]}")()
        pub_key.verify(
            sig,
            data,
            padding.PSS(
                mgf=padding.MGF1(hash_alg), salt_length=padding.PSS.MAX_LENGTH
            ),
            hash_alg,
        )
