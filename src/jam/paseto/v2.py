# -*- coding: utf-8 -*-

import base64
import secrets
from typing import Any, Literal, Optional, Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from jam import BaseEncoder, JsonEncoder
from jam.paseto.__abc_paseto_repo__ import PASETO, BasePASETO
from jam.paseto.utils import __pae__, base64url_encode
from jam.utils.xchacha20poly1305 import xchacha20poly1305_encrypt


class PASETOv2(BasePASETO):
    """PASETO v2 factory."""

    _VERSION = "v2"

    @classmethod
    def key(
        cls: type[PASETO],
        purpose: Literal["local", "public"],
        key: Union[str, bytes],
    ) -> PASETO:
        """Create PASETOv2 instance from provided key."""
        k = cls()
        k._purpose = purpose
        if purpose == "local":
            if isinstance(key, str):
                key = base64.urlsafe_b64decode(key + "==")
            if not isinstance(key, bytes) or len(key) != 32:
                raise ValueError("v2.local key must be 32 bytes")
            k._secret = key
            return k

        elif purpose == "public":
            if isinstance(key, str) and key.startswith("-----BEGIN"):
                private_key = serialization.load_pem_private_key(
                    key.encode(), password=None
                )
                k._secret = private_key
                return k

            elif isinstance(key, str) and "PUBLIC KEY" in key:
                public_key = serialization.load_pem_public_key(key.encode())
                k._public_key = public_key

            elif isinstance(key, (bytes, bytearray)):
                try:
                    public_key = ed25519.Ed25519PublicKey.from_public_bytes(key)
                    k._public_key = public_key
                    return k
                except Exception:
                    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
                        key
                    )
                    k._private_key = private_key
                    k._public_key = private_key.public_key()
                    return k

            raise ValueError("Invalid key for v2.public")

        else:
            raise ValueError("Purpose must be 'local' or 'public'")

    def _encode_local(
        self,
        header: str,
        payload: bytes,
        footer: bytes,  # TODO: Footer checker for specification
    ) -> bytes:
        bheader = header.encode("ascii")
        nonce = secrets.token_bytes(24)
        aad = __pae__([bheader, footer])
        ciphertext = xchacha20poly1305_encrypt(
            self._secret, nonce, payload, aad
        )

        token = (
            bheader
            + base64url_encode(nonce + ciphertext)
            + b"."
            + base64url_encode(footer)
        )
        return token

    def encode(
        self,
        payload: dict[str, Any],
        footer: Optional[Union[dict[str, Any], str]] = None,
        serializer: BaseEncoder = JsonEncoder,
    ) -> str:
        """Encode."""
        header = f"{self._VERSION}.{self._purpose}."
        payload = serializer.dumps(payload)
        footer = serializer.dumps(footer) if footer else b""
        if self._purpose == "local":
            return self._encode_local(header, payload, footer).decode("utf-8")
        else:
            raise NotImplementedError

    def decode(
        self,
        token: str,
        serializer: BaseEncoder = JsonEncoder,
    ) -> tuple[dict[str, Any], Optional[dict[str, Any]]]:
        """Decode."""
        raise NotImplementedError
