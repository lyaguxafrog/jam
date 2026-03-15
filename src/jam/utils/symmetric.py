# -*- coding: utf-8 -*-

import base64
import os


def generate_symmetric_key(n: int = 32) -> str:
    """Generate a N-byte symmetric key.

    Args:
        n (int): Bytes for key

    Returns:
        str: Key
    """
    key = os.urandom(n)
    return base64.urlsafe_b64encode(key).decode("utf-8").rstrip("=")
