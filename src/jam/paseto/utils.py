# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
from datetime import datetime
from typing import Any, Literal, Union
from uuid import uuid4

from jam.paseto import PASETO


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


def init_paseto_instance(
    version: Literal["v1", "v2", "v3", "v4"],
    purpose: Literal["public", "local"],
    key: Union[str, bytes, Any],  # TODO: path to keys
    **kwargs,
) -> PASETO:
    """Init paseto instance.

    Args:
        version (Literal["v1", "v2", "v3", "v4"]): PASETO Version
        purpose (Literal["public", "local"]): Token purpose
        key (str | bytes | Any): Symmetric or asymmetric key
        kwargs: Any key arguments

    Returns:
        BasePaseto: PASETO Instance
    """
    from jam.utils.config_maker import __module_loader__

    # FIXME: Fix custom module init
    if kwargs.get("module", None):
        _paseto: type[PASETO] = __module_loader__(kwargs["module"])
        return _paseto.key(purpose, key)
    else:
        _paseto: type[PASETO] = __module_loader__(
            f"jam.paseto.{version}.PASETO{version}"
        )

    return _paseto.key(purpose, key)


def payload_maker(expire: int, data: dict[str, Any]) -> dict[str, Any]:
    """Generate PASETO payload.

    ```json
    {
        'iat': 1761326685.45693,
        'exp': 1761328485.45693,
        'pit': '52aeaf12-0825-4bc1-aa45-5ded41df2463',
        # custom data
        'user': 1,
        'role': 'admin'
    }
    ```

    Args:
        expire (int): Token lifetime
        data (dict[str, Any]): Custom data

    Returns:
        dict: Payload
    """
    now = datetime.now().timestamp()
    _payload = {"iat": now, "exp": expire + now, "pit": str(uuid4())}

    return _payload | data
