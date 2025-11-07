# -*- coding: utf-8 -*-

import hashlib
import hmac
import os.path
from typing import Any, Literal, Optional, Union

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

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
        secret: Union[
            str,
            bytes,
            rsa.RSAPrivateKey,
            rsa.RSAPublicKey,
        ],
        password: Optional[str] = None,
        serializer: Union[BaseEncoder, type[BaseEncoder]] = JsonEncoder,
    ) -> None:
        """Initialize JWT Factory.

        Args:
            alg (str): Algorithm
            secret (str | bytes | rsa.RSAPrivateKey | rsa.RSAPublicKey): Secret key or path to private/public key file
            password (str | None): Password for asymmetric keys
            serializer (BaseEncoder |type[BaseEncoder]): JSON Serializer
        """
        self.alg = alg
        self.__secret = secret
        self._serializer = serializer
        self.__password = password

    @staticmethod
    def _file_loader(path: str) -> str:
        if not os.path.isfile(path):
            return path
        else:
            with open(path) as f:
                return f.read()

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

        elif self.alg.startswith("ES"):
            curve_map = {
                "ES256": (ec.SECP256R1(), hashes.SHA256()),
                "ES384": (ec.SECP384R1(), hashes.SHA384()),
                "ES512": (ec.SECP521R1(), hashes.SHA512()),
            }
            if self.alg not in curve_map:
                raise ValueError(f"Unsupported ECDSA algorithm: {self.alg}")

            curve, hash_alg = curve_map[self.alg]

            if isinstance(self.__secret, str):
                key_data = self._file_loader(self.__secret)
                private_key = serialization.load_pem_private_key(
                    (
                        key_data.encode()
                        if isinstance(key_data, str)
                        else key_data
                    ),
                    password=(
                        self.__password.encode() if self.__password else None
                    ),
                )
            else:
                private_key = self.__secret

            der_signature = private_key.sign(
                signature_input, ec.ECDSA(hash_alg)
            )
            r, s = decode_dss_signature(der_signature)

            n = (private_key.curve.key_size + 7) // 8
            raw_signature = r.to_bytes(n, "big") + s.to_bytes(n, "big")
            return base64url_encode(raw_signature)
        elif self.alg.startswith("PS"):
            hash_alg = getattr(hashes, f"SHA{self.alg.replace('PS', '')}")()

            if isinstance(self.__secret, str):
                key_data = self._file_loader(self.__secret)
                private_key = serialization.load_pem_private_key(
                    (
                        key_data.encode()
                        if isinstance(key_data, str)
                        else key_data
                    ),
                    password=(
                        self.__password.encode()
                        if isinstance(self.__password, str)
                        else self.__password
                    ),
                )
            else:
                private_key = serialization.load_pem_private_key(
                    self.__secret,
                    password=(
                        self.__password.encode()
                        if isinstance(self.__password, str)
                        else self.__password
                    ),
                )

            # Ensure it's actually an RSA key
            if not isinstance(private_key, rsa.RSAPrivateKey):
                raise TypeError("PS algorithms require an RSA private key")

            signature = private_key.sign(
                signature_input,
                padding.PSS(
                    mgf=padding.MGF1(hash_alg),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hash_alg,
            )
            return base64url_encode(signature)
        else:
            raise ValueError("Unsupported algorithm")

    def encode(
        self,
        payload: dict[str, Any],
    ) -> str:
        """Encode token.

        Args:
            payload (dict[str, Any]): The payload to encode.

        Returns:
            str: The encoded token.
        """
        header = {"typ": "jwt", "alg": self.alg}

        header_encoded = base64url_encode(self._serializer.dumps(header))
        payload_encoder = base64url_encode(self._serializer.dumps(payload))
        signature = self.__sign(f"{header_encoded}.{payload_encoder}".encode())

        return f"{header_encoded}.{payload_encoder}.{signature}"

    def decode(
        self, token: str, public_key: Optional[Any] = None
    ) -> dict[str, Any]:
        """Decode."""
        ...
