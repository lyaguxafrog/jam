# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import secrets
from typing import Any, Literal, Optional, Union

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from jam.__abc_encoder__ import BaseEncoder
from jam.encoders import JsonEncoder
from jam.paseto.__abc_paseto_repo__ import PASETO, BasePASETO, RSAKeyLike
from jam.paseto.utils import (
    __gen_hash__,
    __pae__,
    base64url_decode,
    base64url_encode,
)


class PASETOv1(BasePASETO):
    """Paseto v1 factory."""

    _VERSION = "v1"

    @classmethod
    def key(
        cls: type[PASETO],
        purpose: Literal["local", "public"],
        key: Union[str, bytes, None, RSAPrivateKey],
        public_key: Union[RSAKeyLike] = None,
    ) -> PASETO:
        """Return PASETO instance.

        Args:
            purpose (Literal["local", "public"]): Paseto purpose
            key (str | bytes): PEM or secret key
            public_key (str | bytes | RSAPublicKey | None): Public key for RSA

        Returns:
            PASETO: Paseto instance
        """
        ky = cls()
        if cls._rsa_pem_check(key):
            if purpose == "local":
                raise ValueError("PASETOv1.local does not support RSA keys")
            key = cls.load_rsa_key(key, private=True)
            if not isinstance(key, RSAPrivateKey):
                raise ValueError("Invalid RSA private key")
            ky._secret = key
            ky._public_key = cls.load_rsa_key(public_key, private=False)
        else:
            if purpose == "local":
                if isinstance(key, str):
                    key = base64.urlsafe_b64decode(key + "==")
                if not isinstance(key, bytes) or len(key) != 32:
                    raise ValueError(
                        "PASETOv1.local requires a 32-byte secret key"
                    )
                ky._secret = key
            else:
                raise ValueError("PASETOv1.public requires an RSA private key")
        ky._purpose = purpose
        return ky

    def _encode_local(
        self,
        header: str,
        payload: bytes,
        footer: bytes,
    ) -> bytes:
        header_bytes = header.encode("ascii")
        nonce = secrets.token_bytes(32)
        pl = __gen_hash__(nonce, payload, 32)

        hkdf_params = {
            "algorithm": hashes.SHA384(),
            "length": 32,
            "salt": pl[0:16],
        }
        ek = HKDF(info=b"paseto-encryption-key", **hkdf_params).derive(
            self._secret
        )
        ak = HKDF(info=b"paseto-auth-key-for-aead", **hkdf_params).derive(
            self._secret
        )

        ciphertext = self._encrypt(ek, pl[16:], payload)
        pre_auth = __pae__([header_bytes, pl, ciphertext, footer])
        tag = hmac.new(ak, pre_auth, hashlib.sha384).digest()

        token = header_bytes + base64url_encode(pl + ciphertext + tag)
        if footer:
            token += b"." + base64url_encode(footer)
        return token

    def _encode_public(
        self, header: str, payload: bytes, footer: bytes
    ) -> bytes:
        header_bytes = header.encode("ascii")
        pre_auth = __pae__([header_bytes, payload, footer])

        try:
            signature = self._secret.sign(
                pre_auth,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA384()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA384(),
            )
        except Exception as e:
            raise ValueError(f"Failed to sign PASETO token: {e}")

        token = header_bytes + base64url_encode(payload + signature)
        if footer:
            token += b"." + base64url_encode(footer)
        return token

    def _decode_local(self, token: str, serializer):
        """Decode local PASETO."""
        parts = token.encode("utf-8").split(b".")
        if len(parts) < 3:
            raise ValueError("Invalid token format")

        header = b".".join(parts[:2]) + b"."
        if header != b"v1.local.":
            raise ValueError("Invalid PASETO header")

        payload_part = parts[2]
        footer_part = parts[3] if len(parts) > 3 else b""

        decoded = base64url_decode(payload_part)
        if len(decoded) < 80:
            raise ValueError("Invalid payload size")

        pl = decoded[:32]
        ciphertext_tag = decoded[32:]
        tag = ciphertext_tag[-48:]
        ciphertext = ciphertext_tag[:-48]

        footer_decoded = base64url_decode(footer_part) if footer_part else b""

        hkdf_params = {
            "algorithm": hashes.SHA384(),
            "length": 32,
            "salt": pl[0:16],
        }
        ek = HKDF(info=b"paseto-encryption-key", **hkdf_params).derive(
            self._secret
        )
        ak = HKDF(info=b"paseto-auth-key-for-aead", **hkdf_params).derive(
            self._secret
        )

        pre_auth = __pae__([header, pl, ciphertext, footer_decoded])
        expected_tag = hmac.new(ak, pre_auth, hashlib.sha384).digest()
        if not hmac.compare_digest(tag, expected_tag):
            raise ValueError("Invalid authentication tag")

        payload_bytes = self._decrypt(ek, pl[16:], ciphertext)
        payload = serializer.loads(payload_bytes)

        # FIXME: Optimize
        footer = None
        if footer_decoded:
            try:
                footer = serializer.loads(footer_decoded)
            except Exception:
                try:
                    footer = footer_decoded.decode("utf-8")
                except Exception:
                    footer = footer_decoded

        return payload, footer

    def _decode_public(
        self,
        token: str,
        serializer: Union[type[BaseEncoder], BaseEncoder] = JsonEncoder,
    ):
        parts = token.encode("utf-8").split(b".")
        if len(parts) < 3:
            raise ValueError("Invalid token format")

        header = b".".join(parts[:2]) + b"."
        if header != b"v1.public.":
            raise ValueError("Invalid PASETO header")

        payload_part = parts[2]
        footer_part = parts[3] if len(parts) > 3 else b""

        decoded = base64url_decode(payload_part)
        if len(decoded) < 256:
            raise ValueError("Invalid token body")

        key_size = self._public_key.key_size // 8
        if len(decoded) < key_size:
            raise ValueError("Invalid payload/signature size")

        payload = decoded[:-key_size]
        signature = decoded[-key_size:]

        footer_decoded = base64url_decode(footer_part) if footer_part else b""

        pre_auth = __pae__([header, payload, footer_decoded])
        try:
            self._public_key.verify(
                signature,
                pre_auth,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA384()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA384(),
            )
        except Exception:
            raise ValueError("Invalid signature")

        payload_data = serializer.loads(payload)

        footer = None
        if footer_decoded:
            try:
                footer = serializer.loads(footer_decoded)
            except Exception:
                try:
                    footer = footer_decoded.decode("utf-8")
                except Exception:
                    footer = footer_decoded

        return payload_data, footer

    def encode(
        self,
        payload: dict[str, Any],
        footer: Optional[Union[dict[str, Any], str]] = None,
        serializer: Union[type[BaseEncoder], BaseEncoder] = JsonEncoder,
    ) -> str:
        """Encode PASETO."""
        header = f"{self._VERSION}.{self.purpose}."
        payload = serializer.dumps(payload)
        footer = serializer.dumps(footer) if footer else b""

        if self._purpose == "local":
            return self._encode_local(header, payload, footer).decode("utf-8")
        elif self._purpose == "public":
            return self._encode_public(header, payload, footer).decode("utf-8")
        else:
            raise NotImplementedError

    def decode(
        self,
        token: str,
        serializer: Union[type[BaseEncoder], BaseEncoder] = JsonEncoder,
    ) -> tuple[dict[str, Any], Optional[dict[str, Any]]]:
        """Decode PASETO.

        Args:
            token (str): PASETO
            serializer (BaseEncoder): Json serializer
        """
        if token.startswith(f"{self._VERSION}.local"):
            return self._decode_local(token, serializer)
        elif token.startswith(f"{self._VERSION}.public"):
            return self._decode_public(token, serializer)
        else:
            raise NotImplementedError
