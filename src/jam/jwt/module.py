# -*- coding: utf-8 -*-

import hashlib
import hmac
import os.path
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
        secret: Union[str, bytes, rsa.RSAPrivateKey, rsa.RSAPublicKey],
        password: Optional[str] = None,
        serializer: Union[BaseEncoder, type[BaseEncoder]] = JsonEncoder,
        logger: BaseLogger = logger,
    ) -> None:
        """Initialize JWT factory.

        Args:
            alg (str): The algorithm to use for signing and verifying the JWT.
            secret (str | bytes | rsa.RSAPrivateKey | rsa.RSAPublicKey): The secret key or private key to use for signing and verifying the JWT.
            password (str | None): The password to use for decrypting the private key.
            serializer (BaseEncoder | type[BaseEncoder]): The serializer to use for encoding and decoding the JWT payload.
            logger (BaseLogger): The logger to use for logging messages.
        """
        self.alg = alg
        self.__secret = secret
        self._serializer = serializer
        self.__password = password
        self.__logger = logger

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
                private_key = self.__secret

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
            self.__logger.debug(f"Signature generated: {signature.hex()}")
            return base64url_encode(signature)

        else:
            raise ValueError(f"Unsupported algorithm: {self.alg}")

    def encode(self, payload: dict[str, Any]) -> str:
        """Encode token.

        Args:
            payload (dict[str, Any]): The payload to encode.

        Returns:
            str: The encoded token.
        """
        header = {"typ": "jwt", "alg": self.alg}
        header_encoded = base64url_encode(self._serializer.dumps(header))
        payload_encoded = base64url_encode(self._serializer.dumps(payload))
        signature = self.__sign(f"{header_encoded}.{payload_encoded}".encode())
        return f"{header_encoded}.{payload_encoded}.{signature}"

    def decode(
        self, token: str, public_key: Optional[Any] = None
    ) -> dict[str, Any]:
        """Decode token.

        Args:
            token (str): The JWT token to decode.
            public_key (Optional[Any]): The public key to verify the signature.

        Returns:
            dict[str, Any]: The decoded payload.

        Raises:
            ValueError: If the token is invalid or the signature is invalid.
        """
        try:
            header_b64, payload_b64, signature_b64 = token.split(".")
        except ValueError:
            raise ValueError(
                "Invalid token format. Expected header.payload.signature"
            )

        header = self._serializer.loads(base64url_decode(header_b64))
        payload = self._serializer.loads(base64url_decode(payload_b64))
        signing_input = f"{header_b64}.{payload_b64}".encode()
        signature = base64url_decode(signature_b64)

        self.__logger.debug(f"Signature received: {signature.hex()}")

        alg = header.get("alg")
        if alg != self.alg:
            raise ValueError(
                f"Algorithm mismatch: expected {self.alg}, got {alg}"
            )

        if alg.startswith("HS"):
            self.__logger.debug(f"Signing with HMAC algorithm: {self.alg}")
            key = (
                self.__secret.encode("utf-8")
                if isinstance(self.__secret, str)
                else self.__secret
            )
            hash_alg = getattr(hashlib, f"{alg.replace('HS', 'sha')}")
            expected_signature = hmac.new(key, signing_input, hash_alg).digest()
            if not hmac.compare_digest(signature, expected_signature):
                raise ValueError("Invalid HMAC signature")

        elif alg.startswith("RS"):
            self.__logger.debug(f"Signing with RSA algorithm: {self.alg}")
            key = public_key or self.__secret
            if isinstance(key, str):
                if os.path.isfile(key):
                    with open(key, "rb") as key_file:
                        pub_key = serialization.load_pem_public_key(
                            key_file.read()
                        )
                else:
                    pub_key = serialization.load_pem_public_key(key.encode())
            else:
                pub_key = key

            hash_alg = getattr(hashes, f"SHA{alg.replace('RS', '')}")()
            pub_key.verify(
                signature, signing_input, padding.PKCS1v15(), hash_alg
            )

        elif alg.startswith("ES"):
            self.__logger.debug(f"Verifying with ECDSA algorithm: {self.alg}")
            key = public_key or self.__secret
            if isinstance(key, str):
                key_data = self._file_loader(key)
                pub_key = serialization.load_pem_public_key(
                    key_data.encode() if isinstance(key_data, str) else key_data
                )
            else:
                pub_key = key

            curve_map = {
                "ES256": (ec.SECP256R1(), hashes.SHA256()),
                "ES384": (ec.SECP384R1(), hashes.SHA384()),
                "ES512": (ec.SECP521R1(), hashes.SHA512()),
            }
            curve, hash_alg = curve_map[alg]
            n = (pub_key.curve.key_size + 7) // 8
            r = int.from_bytes(signature[:n], "big")
            s = int.from_bytes(signature[n:], "big")
            der_signature = encode_dss_signature(r, s)
            pub_key.verify(der_signature, signing_input, ec.ECDSA(hash_alg))

        elif alg.startswith("PS"):
            self.__logger.debug(f"Verifying with RSA-PSS algorithm: {self.alg}")
            key = public_key or self.__secret
            if isinstance(key, str):
                key_data = self._file_loader(key)
                pub_key = serialization.load_pem_public_key(
                    key_data.encode() if isinstance(key_data, str) else key_data
                )
            else:
                pub_key = key

            hash_alg = getattr(hashes, f"SHA{alg.replace('PS', '')}")()
            pub_key.verify(
                signature,
                signing_input,
                padding.PSS(
                    mgf=padding.MGF1(hash_alg),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hash_alg,
            )

        else:
            raise ValueError(f"Unsupported algorithm: {alg}")

        return payload
