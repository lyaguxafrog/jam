# -*- coding: utf-8 -*-

import base64
import secrets
from typing import Any, Literal, Optional, Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from jam import BaseEncoder, JsonEncoder
from jam.paseto.__abc_paseto_repo__ import PASETO, BasePASETO
from jam.paseto.utils import __pae__, base64url_decode, base64url_encode
from jam.utils.xchacha20poly1305 import (
    xchacha20poly1305_decrypt,
    xchacha20poly1305_encrypt,
)


class PASETOv2(BasePASETO):
    """PASETO v2 factory."""

    _VERSION = "v2"

    @classmethod
    def key(
        cls: type[PASETO],
        purpose: Literal["local", "public"],
        key: Union[str, bytes, Ed25519PrivateKey, Ed25519PublicKey],
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
            if isinstance(key, Ed25519PrivateKey):
                k._secret = key
                k._public_key = key.public_key()
                return k

            if isinstance(key, Ed25519PublicKey):
                k._secret = None
                k._public_key = key
                return k

            if isinstance(key, str):
                key = key.encode()

            try:
                private_key = serialization.load_pem_private_key(
                    key, password=None
                )
                if not isinstance(private_key, Ed25519PrivateKey):
                    raise ValueError("Expected Ed25519 private key")
                k._secret = private_key
                k._public_key = private_key.public_key()
                return k
            except Exception:
                try:
                    public_key = serialization.load_pem_public_key(key)
                    if not isinstance(public_key, Ed25519PublicKey):
                        raise ValueError("Expected Ed25519 public key")
                    k._secret = None
                    k._public_key = public_key
                    return k
                except Exception:
                    raise ValueError("Invalid Ed25519 key provided")

        else:
            raise ValueError("Purpose must be 'local' or 'public'")

    def _encode_local(
        self,
        header: str,
        payload: bytes,
        footer: Optional[bytes],
    ) -> bytes:
        bheader = header.encode("ascii")
        bfooter = footer or b""
        nonce = secrets.token_bytes(24)
        aad = __pae__([bheader, bfooter])

        ciphertext = xchacha20poly1305_encrypt(
            self._secret, nonce, payload, aad
        )

        token = bheader + base64url_encode(nonce + ciphertext)
        if bfooter:
            token += b"." + base64url_encode(bfooter)
        return token

    def _encode_public(
        self, header: str, payload: bytes, footer: Optional[bytes]
    ) -> bytes:
        bheader = header.encode("ascii")
        footer_bytes = footer or b""

        if not isinstance(self._secret, Ed25519PrivateKey):
            raise TypeError(
                "Secret key must be Ed25519PrivateKey for v2.public"
            )

        pre_auth = __pae__([bheader, payload, footer_bytes])
        signature = self._secret.sign(pre_auth)

        token = bheader + base64url_encode(payload + signature)
        if footer_bytes:
            token += b"." + base64url_encode(footer_bytes)
        return token

    def _decode_local(
        self, token: str, serializer: Union[type[BaseEncoder], BaseEncoder]
    ) -> tuple[dict[str, Any], Optional[dict[str, Any]]]:
        parts = token.encode().split(b".")
        if len(parts) < 3:
            raise ValueError("Invalid token format")

        header = b".".join(parts[:2]) + b"."
        if header != b"v2.local.":
            raise ValueError("Invalid header")

        body = base64url_decode(parts[2])
        footer = base64url_decode(parts[3]) if len(parts) > 3 else b""

        nonce = body[:24]
        ciphertext = body[24:]
        aad = __pae__([header, footer])

        try:
            plaintext = xchacha20poly1305_decrypt(
                self._secret, nonce, ciphertext, aad
            )
        except Exception:
            raise ValueError("Invalid authentication or corrupt ciphertext")

        payload = serializer.loads(plaintext)

        footer_val = None
        if footer:
            try:
                footer_val = serializer.loads(footer)
            except Exception:
                try:
                    footer_val = footer.decode("utf-8")
                except Exception:
                    footer_val = footer

        return payload, footer_val

    def _decode_public(
        self,
        token: str,
        serializer,
    ) -> tuple[dict[str, Any], Optional[dict[str, Any]]]:
        parts = token.encode().split(b".")
        if len(parts) < 3:
            raise ValueError("Invalid token format")

        header = b".".join(parts[:2]) + b"."
        if header != b"v2.public.":
            raise ValueError("Invalid header")

        body = base64url_decode(parts[2])
        footer = base64url_decode(parts[3]) if len(parts) > 3 else b""

        if len(body) < 64:
            raise ValueError(
                "Invalid token: too short to contain Ed25519 signature"
            )

        payload = body[:-64]
        signature = body[-64:]
        pre_auth = __pae__([header, payload, footer])

        if not isinstance(self._public_key, Ed25519PublicKey):
            raise TypeError("Public key must be Ed25519PublicKey for v2.public")

        try:
            self._public_key.verify(signature, pre_auth)
        except Exception:
            raise ValueError("Invalid signature")

        payload_data = serializer.loads(payload)

        footer_val = None
        if footer:
            try:
                footer_val = serializer.loads(footer)
            except Exception:
                try:
                    footer_val = footer.decode("utf-8")
                except Exception:
                    footer_val = footer

        return payload_data, footer_val

    def encode(
        self,
        payload: dict[str, Any],
        footer: Optional[Union[dict[str, Any], str]] = None,
        serializer: BaseEncoder = JsonEncoder,
    ) -> str:
        """Encode."""
        header = f"{self._VERSION}.{self._purpose}."
        payload = serializer.dumps(payload)
        footer = serializer.dumps(footer) if footer else None
        if self._purpose == "local":
            return self._encode_local(header, payload, footer).decode("utf-8")
        elif self._purpose == "public":
            return self._encode_public(header, payload, footer).decode("utf-8")
        else:
            raise NotImplementedError

    def decode(
        self,
        token: str,
        serializer: BaseEncoder = JsonEncoder,
    ) -> tuple[dict[str, Any], Optional[dict[str, Any]]]:
        """Decode."""
        if token.startswith(f"{self._VERSION}.local"):
            return self._decode_local(token, serializer)
        elif token.startswith(f"{self._VERSION}.public"):
            return self._decode_public(token, serializer)
        else:
            raise NotImplementedError
