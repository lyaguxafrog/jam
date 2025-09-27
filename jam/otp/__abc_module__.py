# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import struct
import urllib.parse
from dataclasses import dataclass
from typing import Literal, Optional, Union


class BaseOTP:
    """Base *OTP."""

    def __init__(
        self,
        secret: Union[bytes, str],
        digits: int = 6,
        digest: Literal["sha1", "sha256", "sha512"] = "sha1",
    ) -> None:
        """Class constructor.

        Args:
            secret (bytes | str): Secret key(str or Byte32).
            digits (int, optional): Number of digits in the code. Default is 6.
            digest (str, optional): Hash algorithm (sha1, sha256, sha512). Default is `sha1`.
        """
        if isinstance(secret, str):
            secret = base64.b32decode(secret.upper() + "=" * (-len(secret) % 8))
        self._secret = secret
        self.digits = digits
        self.digest = digest

    def _dynamic_truncate(self, hmac_digest: bytes) -> int:
        """Performs dynamic truncation according to RFC4226.

        See: https://datatracker.ietf.org/doc/html/rfc4226

        Args:
            hmac_digest (bytes): HMAC-hash.

        Returns:
            int: Number truncated to 31 bits.
        """
        offset = hmac_digest[-1] & 0x0F
        code = (
            ((hmac_digest[offset] & 0x7F) << 24)
            | (hmac_digest[offset + 1] << 16)
            | (hmac_digest[offset + 2] << 8)
            | (hmac_digest[offset + 3])
        )
        return code % (10**self.digits)

    def _hmac(self, counter: int) -> bytes:
        """Calculates HMAC from counter.

        Args:
            counter (int): Counter (HOTP) or the calculated interval number (TOTP).

        Returns:
            bytes: HMAC.
        """
        h = hmac.new(
            self._secret,
            struct.pack(">Q", counter),
            getattr(hashlib, self.digest),
        )
        return h.digest()

    def provisioning_uri(
        self,
        name: str,
        issuer: str,
        type_: str = "totp",
        counter: Optional[int] = None,
    ) -> str:
        """Generates an otpauth:// URI for Google Authenticator.

        Args:
            name (str): Account name (e.g., email).
            issuer (str): Service name (e.g., "GitHub").
            type_ (str, optional): OTP type (“totp” or 'hotp'). Default is "totp".
            counter (int | None, optional): Counter (for HOTP). Default is None.

        Returns:
            str: A string of the form "otpauth://..."
        """
        label = urllib.parse.quote(f"{issuer}:{name}")
        params = {
            "secret": base64.b32encode(self._secret)
            .decode("utf-8")
            .replace("=", ""),
            "issuer": issuer,
            "algorithm": self.digest.upper(),
            "digits": str(self.digits),
        }
        if type_ == "hotp" and counter is not None:
            params["counter"] = str(counter)
        query = urllib.parse.urlencode(params)
        return f"otpauth://{type_}/{label}?{query}"


@dataclass
class OTPConfig:
    """Config for Jam instance."""

    type: str
    digits: int
    digest: Literal["sha1", "sha256", "sha512"]
