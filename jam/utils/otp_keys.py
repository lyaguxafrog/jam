# -*- coding: utf-8 -*-

import base64
import hashlib
import math
import secrets


def generate_otp_key(entropy_bits: int = 128) -> str:
    """Generate generic OTP secret key.

    Args:
        entropy_bits (int): Entropy bits to key

    Returns:
        str
    """
    if entropy_bits < 40:
        raise ValueError("Minimum 40 bits of entropy (≥ 80 recommended).")

    num_bytes = math.ceil(entropy_bits / 8)
    raw = secrets.token_bytes(num_bytes)

    b32 = base64.b32encode(raw).decode("ascii")
    return b32.rstrip("=").upper()


def otp_key_from_string(s: str) -> str:
    """Generate OTP-valid key from string.

    Args:
        s (str): String for key

    Returns:
        bytes: OTP key

    Example:
        ```python
        >>> from jam.utils import otp_key_from_string
        >>> user_email: str = "some.email@mail.com"
        >>> key = otp_key_from_string(user_email)
        >>> print(key)
        'O54O6YRKTH3IPNEBIUMKMK3FZ35OF6Q5'
        ```
    """
    hashed = hashlib.sha1(s.encode()).digest()
    key = base64.b32encode(hashed).decode("utf-8").rstrip("=")
    return key
