# -*- coding: utf-8 -*-

import hashlib
import hmac
import json
from typing import Any

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)

from jam.exceptions import JamJWTUnsupportedAlgorithm
from jam.jose.__algorithms__ import SUPPORTED_ALGORITHMS
from jam.jose.__base__ import BaseJWS
from jam.jose.utils import __base64url_decode__, __base64url_encode__


class JWS(BaseJWS):
    """JWS (JSON Web Signature) implementation."""

    _SUPPORTED_ALGORITHMS = SUPPORTED_ALGORITHMS

    def __init__(
        self,
        alg: str,
        key: str | bytes,
    ) -> None:
        """Initialize the JWS object.

        Args:
            alg (str): Algorithm name
            key (str | bytes): Key to use for signing/verifying
        """
        self._alg = alg.upper()
        self._validate_algorithm(self._alg)

        if isinstance(key, str):
            key = key.encode()

        self._key = key

        self._private_key = None
        self._public_key = None

        if self._alg.startswith(("RS", "PS", "ES")):
            try:
                self._private_key = load_pem_private_key(key, password=None)
                self._public_key = self._private_key.public_key()
            except Exception:
                self._public_key = load_pem_public_key(key)

    def _validate_algorithm(self, alg: str) -> None:
        """Validate algorithm name.

        Args:
            alg (str): Algorithm name

        Raises:
            JamJWTUnsupportedAlgorithm: If algorithm is not supported
        """
        if alg not in self._SUPPORTED_ALGORITHMS:
            raise JamJWTUnsupportedAlgorithm(
                details={
                    "algorithm": alg,
                    "supported_algorithms": self._SUPPORTED_ALGORITHMS,
                }
            )

    def _hash(self):
        return {
            "256": hashes.SHA256(),
            "384": hashes.SHA384(),
            "512": hashes.SHA512(),
        }[self._alg[-3:]]

    def _sign_bytes(self, signing_input: bytes) -> bytes:
        if self._alg.startswith("HS"):
            digestmod = {
                "256": hashlib.sha256,
                "384": hashlib.sha384,
                "512": hashlib.sha512,
            }[self._alg[-3:]]
            return hmac.new(self._key, signing_input, digestmod).digest()

        elif self._alg.startswith("RS"):
            if not self._private_key:
                raise ValueError("Private key required for signing")
            return self._private_key.sign(  # type: ignore
                signing_input,
                padding.PKCS1v15(),  # type: ignore
                self._hash(),  # type: ignore
            )

        elif self._alg.startswith("PS"):
            if not self._private_key:
                raise ValueError("Private key required for signing")
            return self._private_key.sign(  # type: ignore
                signing_input,
                padding.PSS(  # type: ignore
                    mgf=padding.MGF1(self._hash()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                self._hash(),  # type: ignore
            )

        elif self._alg.startswith("ES"):
            if not self._private_key:
                raise ValueError("Private key required for signing")
            return self._private_key.sign(  # type: ignore
                signing_input,
                ec.ECDSA(self._hash()),  # type: ignore
            )

        raise ValueError("Unsupported algorithm")

    def _verify_bytes(self, signing_input: bytes, signature: bytes) -> None:
        if self._alg.startswith("HS"):
            digestmod = {
                "256": hashlib.sha256,
                "384": hashlib.sha384,
                "512": hashlib.sha512,
            }[self._alg[-3:]]
            expected = hmac.new(self._key, signing_input, digestmod).digest()
            if not hmac.compare_digest(expected, signature):
                raise Exception("Invalid signature")

        elif self._alg.startswith("RS"):
            self._public_key.verify(  # type: ignore
                signature,
                signing_input,
                padding.PKCS1v15(),  # type: ignore
                self._hash(),  # type: ignore
            )

        elif self._alg.startswith("PS"):
            self._public_key.verify(  # type: ignore
                signature,
                signing_input,
                padding.PSS(  # type: ignore
                    mgf=padding.MGF1(self._hash()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                self._hash(),  # type: ignore
            )

        elif self._alg.startswith("ES"):
            self._public_key.verify(  # type: ignore
                signature,
                signing_input,
                ec.ECDSA(self._hash()),  # type: ignore
            )

    def sign(self, header: dict[str, Any] | None, data: dict[str, Any]) -> str:
        """Sign the given data and return the JWS.

        Args:
            header (dict[str, Any] | None): The header to include in the JWS.
            data (dict[str, Any]): The data to sign.

        Returns:
            str: The JWS.
        """
        _header = {
            "alg": self._alg,
        }
        if header:
            _header.update(header)

        header_b64 = __base64url_encode__(
            json.dumps(_header, separators=(",", ":")).encode()
        )
        payload_b64 = __base64url_encode__(
            json.dumps(data, separators=(",", ":")).encode()
        )

        signing_input = f"{header_b64}.{payload_b64}".encode()
        signature = self._sign_bytes(signing_input)

        return f"{header_b64}.{payload_b64}.{__base64url_encode__(signature)}"

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
        try:
            header_b64, payload_b64, signature_b64 = jws.split(".")
        except ValueError:
            raise Exception("Invalid JWS format")

        signing_input = f"{header_b64}.{payload_b64}".encode()
        signature = __base64url_decode__(signature_b64)

        if verify:
            try:
                self._verify_bytes(signing_input, signature)
            except Exception as e:
                raise Exception("Signature verification failed") from e

        return {
            "header": json.loads(__base64url_decode__(header_b64).decode()),
            "payload": json.loads(__base64url_decode__(payload_b64).decode()),
        }
