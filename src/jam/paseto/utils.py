# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac


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
