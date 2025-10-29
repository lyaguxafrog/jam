# -*- coding: utf-8 -*-

import hashlib
import hmac
import os.path
from typing import Any, Literal, Optional, Union

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from jam.encoders import BaseEncoder, JsonEncoder
from jam.jwt.__base__ import BaseJWT
from jam.jwt.utils import base64url_encode


class JWT(BaseJWT):
    """JWT Factory."""

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
        secret: Union[str, rsa.RSAPrivateKey, rsa.RSAPublicKey],
        password: Optional[str] = None,
        serializer: Union[BaseEncoder, type[BaseEncoder]] = JsonEncoder,
    ) -> None:
        """Initialize JWT Factory.

        Args:
            alg (str): Algorithm
            secret (str | rsa.RSAPrivateKey | rsa.RSAPublicKey): Secret key or path to private/public key file
            password (str | None): Password for asymmetric keys
            serializer (BaseEncoder |type[BaseEncoder]): JSON Serializer
        """
        self.alg = alg
        self.__secret = secret
        self.serializer = serializer
        self.__password = password

    def __sign(self, signature_input: bytes) -> str:
        if self.alg.startswith("HS"):
            hash_alg = getattr(hashlib, f"{self.alg.replace('HS', 'sha')}")
            signature = hmac.new(
                self.__secret.encode("utf-8"), signature_input, hash_alg
            ).digest()
            return base64url_encode(signature)
        elif self.alg.startswith("RS"):
            if isinstance(self.__secret, str):
                if os.path.isfile(self.__secret):
                    with open(self.__secret, "rb") as key_file:
                        private_key = serialization.load_pem_private_key(
                            key_file.read(),
                            password=self.__password,
                        )
                else:
                    private_key = serialization.load_pem_private_key(
                        self.__secret.encode(),
                        password=self.__password,
                    )
            else:
                private_key = self.__secret
            hash_alg = getattr(hashes, f"SHA{self.alg.replace('RS', '')}")()
            signature = private_key.sign(
                signature_input, padding.PKCS1v15(), hash_alg
            )
            return base64url_encode(signature)
        else:
            raise ValueError("Unsupported algorithm")

    def encode(
        self,
        payload: dict[str, Any],
    ) -> str:
        """Encode."""
        header = {"typ": "jwt", "alg": self.alg}

        header_encoded = base64url_encode(self.serializer.dumps(header))
        payload_encoder = base64url_encode(self.serializer.dumps(payload))
        signature = self.__sign(f"{header_encoded}.{payload_encoder}".encode())

        return f"{header_encoded}.{payload_encoder}.{signature}"

    def decode(
        self, token: str, public_key: Optional[Any] = None
    ) -> dict[str, Any]:
        """Decode."""
        ...
