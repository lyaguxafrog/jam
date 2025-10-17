# -*- coding: utf-8 -*-

import secrets
from typing import Any, Literal, Optional, Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from jam.__abc_encoder__ import BaseEncoder
from jam.encoders import JsonEncoder
from jam.paseto.__abc_paseto_repo__ import PASETO, BasePASETO
from jam.paseto.utils import __pae__, base64url_decode, base64url_encode
from jam.utils.xchacha20poly1305 import (
    xchacha20poly1305_decrypt,
    xchacha20poly1305_encrypt,
)


class PASETOv4(BasePASETO):
    """PASETO v4 factory."""

    _VERSION = "v4"

    @classmethod
    def key(
        cls: type[PASETO],
        purpose: Literal["local", "public"],
        key: Union[str, bytes, Ed25519PrivateKey],
    ) -> PASETO:
        """Create PASETO Factory.

        Args:
            purpose (Literal["local", "public"]): PASETO type
            key (str | bytes | Ed25519PrivateKey): Secret or ED Private key
        """
        inst = cls()
        inst._purpose = purpose

        if purpose == "local":
            if isinstance(key, str):
                raw = base64url_decode(key.encode("utf-8"))
            else:
                raw = key
            if not isinstance(raw, (bytes, bytearray)) or len(raw) != 32:
                raise ValueError("v4.local requires a 32-byte secret key")
            inst._secret = bytes(raw)
            return inst

        elif purpose == "public":
            # Ed25519 objects
            if isinstance(key, Ed25519PrivateKey):
                inst._secret = key
                inst._public_key = key.public_key()
                return inst
            if isinstance(key, Ed25519PublicKey):
                inst._secret = None
                inst._public_key = key
                return inst

            key_bytes = key.encode("utf-8") if isinstance(key, str) else key
            try:
                priv = serialization.load_pem_private_key(
                    key_bytes, password=None
                )
                if isinstance(priv, Ed25519PrivateKey):
                    inst._secret = priv
                    inst._public_key = priv.public_key()
                    return inst
            except Exception:
                pass
            try:
                priv = serialization.load_der_private_key(
                    key_bytes, password=None
                )
                if isinstance(priv, Ed25519PrivateKey):
                    inst._secret = priv
                    inst._public_key = priv.public_key()
                    return inst
            except Exception:
                pass
            try:
                pub = serialization.load_pem_public_key(key_bytes)
                if isinstance(pub, Ed25519PublicKey):
                    inst._secret = None
                    inst._public_key = pub
                    return inst
            except Exception:
                pass
            try:
                pub = serialization.load_der_public_key(key_bytes)
                if isinstance(pub, Ed25519PublicKey):
                    inst._secret = None
                    inst._public_key = pub
                    return inst
            except Exception:
                pass

            raise ValueError("Invalid Ed25519 key for v4.public")
        else:
            raise ValueError("Purpose must be 'local' or 'public'")

    def encode(
        self,
        payload: dict[str, Any],
        footer: Optional[Union[dict[str, Any], str, bytes]] = None,
        serializer: Union[type[BaseEncoder], BaseEncoder] = JsonEncoder,
    ) -> str:
        """Encode PASETO.

        Args:
            payload (dict[str, Any]): PASETO Payload
            footer (dict[str, Any] | str | None): Footer if needed
            serializer (type[BaseEncoder] | BaseEncoder): JSON Serializer

        Returns:
            str: PASETO
        """
        header = f"{self._VERSION}.{self._purpose}."
        payload_bytes = serializer.dumps(payload)

        if isinstance(footer, (dict, list)):
            footer_bytes = serializer.dumps(footer)
        elif isinstance(footer, str):
            footer_bytes = footer.encode("utf-8")
        elif isinstance(footer, (bytes, bytearray)):
            footer_bytes = bytes(footer)
        else:
            footer_bytes = b""

        if self._purpose == "local":
            return self._encode_local(
                header, payload_bytes, footer_bytes
            ).decode("utf-8")
        elif self._purpose == "public":
            return self._encode_public(
                header, payload_bytes, footer_bytes
            ).decode("utf-8")
        else:
            raise NotImplementedError

    def decode(
        self,
        token: str,
        serializer: Union[type[BaseEncoder], BaseEncoder] = JsonEncoder,
    ) -> tuple[dict[str, Any], Optional[Union[dict[str, Any], str, bytes]]]:
        """Decode PASETO.

        Args:
            token (str): PASETO
            serializer (type[BaseEncoder] | BaseEncoder]): JSON Serializer
        """
        if token.startswith(f"{self._VERSION}.local."):
            return self._decode_local(token, serializer)
        elif token.startswith(f"{self._VERSION}.public."):
            return self._decode_public(token, serializer)
        else:
            raise NotImplementedError

    def _encode_local(
        self, header: str, payload: bytes, footer: bytes
    ) -> bytes:
        header_b = header.encode("ascii")
        nonce = secrets.token_bytes(24)
        aad = __pae__([header_b, footer or b""])
        ciphertext = xchacha20poly1305_encrypt(
            self._secret, nonce, payload, aad
        )

        token = header_b + base64url_encode(nonce + ciphertext)
        if footer:
            token += b"." + base64url_encode(footer)
        return token

    def _decode_local(
        self, token: str, serializer: Union[type[BaseEncoder], BaseEncoder]
    ):
        parts = token.encode("utf-8").split(b".")
        if len(parts) < 3:
            raise ValueError("Invalid token format")
        header = b".".join(parts[:2]) + b"."
        if header != b"v4.local.":
            raise ValueError("Invalid header")

        body = base64url_decode(parts[2])
        if len(body) < 24 + 16:
            raise ValueError("Invalid token body")

        nonce = body[:24]
        ciphertext = body[24:]
        footer_part = parts[3] if len(parts) > 3 else b""
        footer_decoded = base64url_decode(footer_part) if footer_part else b""

        aad = __pae__([header, footer_decoded])
        try:
            plaintext = xchacha20poly1305_decrypt(
                self._secret, nonce, ciphertext, aad
            )
        except Exception:
            raise ValueError("Invalid authentication or corrupt ciphertext")

        payload = serializer.loads(plaintext)

        footer_val = None
        if footer_decoded:
            try:
                footer_val = serializer.loads(footer_decoded)
            except Exception:
                try:
                    footer_val = footer_decoded.decode("utf-8")
                except Exception:
                    footer_val = footer_decoded

        return payload, footer_val

    def _encode_public(
        self, header: str, payload: bytes, footer: bytes
    ) -> bytes:
        if not hasattr(self._secret, "sign") or not isinstance(
            self._secret, Ed25519PrivateKey
        ):
            raise ValueError(
                "Private Ed25519 key required for v4.public signing"
            )
        header_b = header.encode("ascii")
        pre_auth = __pae__([header_b, payload, footer or b""])
        signature = self._secret.sign(pre_auth)  # raw 64 bytes

        token = header_b + base64url_encode(payload + signature)
        if footer:
            token += b"." + base64url_encode(footer)
        return token

    def _decode_public(self, token: str, serializer: BaseEncoder):
        parts = token.encode("utf-8").split(b".")
        if len(parts) < 3:
            raise ValueError("Invalid token format")
        header = b".".join(parts[:2]) + b"."
        if header != b"v4.public.":
            raise ValueError("Invalid header")

        body = base64url_decode(parts[2])
        if len(body) < 64:
            raise ValueError(
                "Invalid token body (too short for Ed25519 signature)"
            )
        payload = body[:-64]
        signature = body[-64:]
        footer_part = parts[3] if len(parts) > 3 else b""
        footer_decoded = base64url_decode(footer_part) if footer_part else b""

        pre_auth = __pae__([header, payload, footer_decoded])

        if not self._public_key:
            raise ValueError("Public key required for v4.public verification")
        try:
            # raises InvalidSignature on failure
            self._public_key.verify(signature, pre_auth)
        except Exception:
            raise ValueError("Invalid signature")

        payload_data = serializer.loads(payload)

        footer_val = None
        if footer_decoded:
            try:
                footer_val = serializer.loads(footer_decoded)
            except Exception:
                try:
                    footer_val = footer_decoded.decode("utf-8")
                except Exception:
                    footer_val = footer_decoded

        return payload_data, footer_val
