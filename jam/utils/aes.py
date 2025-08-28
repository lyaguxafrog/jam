# -*- coding: utf-8 -*-

from cryptography.fernet import Fernet


def generate_aes_key() -> bytes:
    """Generate a new AES key."""
    return Fernet.generate_key()
