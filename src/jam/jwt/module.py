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
        secret: Union[
            str,
            bytes,
            rsa.RSAPrivateKey,
            rsa.RSAPublicKey,
        ],
        password: Optional[str] = None,
        serializer: Union[BaseEncoder, type[BaseEncoder]] = JsonEncoder,
        logger: BaseLogger = logger,
    ) -> None:
        """Initialize JWT Factory.

        Args:
            alg (str): Algorithm
            secret (str | bytes | rsa.RSAPrivateKey | rsa.RSAPublicKey): Secret key or path to private/public key file
            password (str | None): Password for asymmetric keys
            serializer (BaseEncoder |type[BaseEncoder]): JSON Serializer
            logger (BaseLogger): Logger instance
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
            self.__logger.debug(f"Signing with algorithm: {self.alg}")
            hash_alg = getattr(hashlib, f"{self.alg.replace('HS', 'sha')}")

            if isinstance(self.__secret, str):
                key = self.__secret.encode("utf-8")
            elif isinstance(self.__secret, bytes):
                key = self.__secret
            else:
                raise TypeError(
                    "Invalid secret type for HMAC algorithm. Expected str or bytes."
                )

            signature = hmac.new(key, signature_input, hash_alg).digest()
            self.__logger.debug(f"Generated signature: {signature.hex()}")
            return base64url_encode(signature)

        elif self.alg.startswith("RS"):
            self.__logger.debug(f"Signing with algorithm: {self.alg}")
            if isinstance(self.__secret, str):
                if os.path.isfile(self.__secret):
                    with open(self.__secret, "rb") as key_file:
                        private_key = serialization.load_pem_private_key(
                            key_file.read(),
                            password=(
                                self.__password.encode()
                                if isinstance(self.__password, str)
                                else self.__password
                            ),
                        )
                else:
                    private_key = serialization.load_pem_private_key(
                        self.__secret.encode(),
                        password=(
                            self.__password.encode()
                            if isinstance(self.__password, str)
                            else self.__password
                        ),
                    )
            else:
                private_key = self.__secret

            hash_alg = getattr(hashes, f"SHA{self.alg.replace('RS', '')}")()
            signature = private_key.sign(
                signature_input, padding.PKCS1v15(), hash_alg
            )
            return base64url_encode(signature)

        elif self.alg.startswith("ES"):
            self.__logger.debug(f"Signing with algorithm: {self.alg}")
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
                        self.__password.encode()
                        if isinstance(self.__password, str)
                        else self.__password
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
            return base64url_encode(signature)

        else:
            raise ValueError(f"Unsupported algorithm: {self.alg}")

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
        """Decode and verify JWT token.

        Args:
            token (str): The token to decode.
            public_key (Optional[Any], optional): The public key to use for verification. Defaults to None.

        Returns:
            dict[str, Any]: The decoded payload.

        Raises:
            ValueError: If the token is invalid or the signature check fails.
        """
        try:
            header_b64, payload_b64, signature_b64 = token.split(".")
        except ValueError:
            raise ValueError(
                "Invalid token format. Expected header.payload.signature"
            )

        self.__logger.debug("Decoding JWT token...")

        # Decode header & payload
        try:
            header = self._serializer.loads(base64url_decode(header_b64))
            payload = self._serializer.loads(base64url_decode(payload_b64))
        except Exception as e:
            raise ValueError(f"Failed to decode token: {e}")

        # Reconstruct signing input
        signing_input = f"{header_b64}.{payload_b64}".encode()
        signature = base64url_decode(signature_b64)

        # --- Verify signature ---
        alg = header.get("alg")
        if alg != self.alg:
            raise ValueError(
                f"Algorithm mismatch: expected {self.alg}, got {alg}"
            )

        self.__logger.debug(f"Verifying signature using algorithm: {alg}")

        # HMAC verification
        if alg.startswith("HS"):
            if isinstance(self.__secret, str):
                key = self.__secret.encode("utf-8")
            elif isinstance(self.__secret, bytes):
                key = self.__secret
            else:
                raise TypeError("Invalid secret type for HMAC algorithm")

            hash_alg = getattr(hashlib, f"{alg.replace('HS', 'sha')}")
            expected_signature = hmac.new(key, signing_input, hash_alg).digest()

            if not hmac.compare_digest(signature, expected_signature):
                raise ValueError("Invalid HMAC signature")

        # RSA verification
        elif alg.startswith("RS"):
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
            try:
                pub_key.verify(
                    signature, signing_input, padding.PKCS1v15(), hash_alg
                )
            except Exception:
                raise ValueError("Invalid RSA signature")

        # ECDSA verification
        elif alg.startswith("ES"):
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

            # split signature into r/s
            n = (pub_key.curve.key_size + 7) // 8
            r = int.from_bytes(signature[:n], "big")
            s = int.from_bytes(signature[n:], "big")
            der_signature = ec.encode_dss_signature(r, s)

            try:
                pub_key.verify(der_signature, signing_input, ec.ECDSA(hash_alg))
            except Exception:
                raise ValueError("Invalid ECDSA signature")

        # RSA-PSS verification
        elif alg.startswith("PS"):
            key = public_key or self.__secret
            if isinstance(key, str):
                key_data = self._file_loader(key)
                pub_key = serialization.load_pem_public_key(
                    key_data.encode() if isinstance(key_data, str) else key_data
                )
            else:
                pub_key = key

            hash_alg = getattr(hashes, f"SHA{alg.replace('PS', '')}")()

            try:
                pub_key.verify(
                    signature,
                    signing_input,
                    padding.PSS(
                        mgf=padding.MGF1(hash_alg),
                        salt_length=padding.PSS.MAX_LENGTH,
                    ),
                    hash_alg,
                )
            except Exception:
                raise ValueError("Invalid RSA-PSS signature")

        else:
            raise ValueError(f"Unsupported algorithm: {alg}")

        self.__logger.debug("JWT verification successful.")
        return payload
