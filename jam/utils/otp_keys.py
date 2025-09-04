# -*- coding: utf-8 -*-

import base64
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
