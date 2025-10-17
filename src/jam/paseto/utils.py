# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
from typing import Union


def __b64url_nopad__(b: bytes) -> str:
    """Return B64 nopad."""
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def __gen_hash__(key: bytes, msg: bytes, hash_size: int = 0) -> bytes:
    """Generate hash."""
    try:
        hash_ = hmac.new(key, msg, hashlib.sha384).digest()
        return hash_[0:hash_size] if hash_size > 0 else hash_
    except Exception as e:
        raise ValueError(f"Failed to generate hash: {e}")


def __pae__(pieces: list[bytes]) -> bytes:
    """Pre-Authentication Encoding (PAE) as per PASETO spec."""

    def le64(n: int) -> bytes:
        s = bytearray(8)
        for i in range(8):
            if i == 7:
                n = n & 127
            s[i] = n & 255
            n = n >> 8
        return bytes(s)

    output = le64(len(pieces))
    for piece in pieces:
        output += le64(len(piece))
        output += piece
    return output


def base64url_decode(v: Union[str, bytes]) -> bytes:
    """Base64 URL-safe decoding with padding."""
    if isinstance(v, bytes):
        bv = v
    else:
        bv = v.encode("ascii")
    rem = len(bv) % 4
    if rem > 0:
        bv += b"=" * (4 - rem)
    return base64.urlsafe_b64decode(bv)


def base64url_encode(data: Union[bytes, str]) -> bytes:
    """Base64 URL-safe encoding without padding."""
    if isinstance(data, bytes):
        bv = data
    else:
        bv = data.encode("ascii")
    return base64.urlsafe_b64encode(bv).replace(b"=", b"")
