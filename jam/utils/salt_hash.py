# -*- coding: utf-8 -*-
"""Utilities for secure password hashing and verification. Uses PBKDF2-HMAC-SHA256 with salt and constant-time comparison."""

import hashlib
import hmac
import os
from typing import Optional


def hash_password(
    password: str,
    salt: Optional[bytes] = None,
    iterations: int = 100_000,
    salt_size: int = 16,
) -> tuple[str, str]:
    """Hashes a password with a salt using PBKDF2-HMAC-SHA256.

    Args:
        password (str): Password to hash.
        salt (bytes | None): Salt. If None, a random salt is generated.
        iterations (int): Number of PBKDF2 iterations.
        salt_size (int): Size of the random salt in bytes.

    Returns:
        tuple[str, str]: (hex_salt, hex_hash)

    Example:
        ```python
        >>> salt, hash_ = hash_password("my_password")
        >>> isinstance(salt, str)
        True
        >>> isinstance(hash_, str)
        True

        # Using custom iterations and salt size
        >>> salt, hash_ = hash_password("my_password", iterations=150_000, salt_size=24)
        ```
    """
    if salt is None:
        salt = os.urandom(salt_size)

    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )

    return salt.hex(), pwd_hash.hex()


def check_password(
    password: str, salt_hex: str, hash_hex: str, iterations: int = 100_000
) -> bool:
    """Verifies a password by recalculating the hash and comparing it to the stored hash.

    Args:
        password (str): Password to verify.
        salt_hex (str): Hex representation of the salt.
        hash_hex (str): Hex representation of the stored hash.
        iterations (int): Number of PBKDF2 iterations, must match the hashing call.

    Returns:
        bool: True if the password is correct, False otherwise.

    Example:
        ```python
        >>> salt, hash_ = hash_password("my_password")
        >>> check_password("my_password", salt, hash_)
        True
        >>> check_password("wrong_password", salt, hash_)
        False

        # Using custom iterations
        >>> salt, hash_ = hash_password("my_password", iterations=150_000)
        >>> check_password("my_password", salt, hash_, iterations=150_000)
        True
        ```
    """
    salt = bytes.fromhex(salt_hex)
    stored_hash = bytes.fromhex(hash_hex)

    new_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )

    return hmac.compare_digest(new_hash, stored_hash)


def serialize_hash(salt_hex: str, hash_hex: str) -> str:
    """Combines salt and hash into a single string for database storage.

    Example:
        ```python
        >>> salt, hash_ = hash_password("my_password")
        >>> serialized = serialize_hash(salt, hash_)
        >>> isinstance(serialized, str)
        True
        ```
    """
    return f"{salt_hex}${hash_hex}"


def deserialize_hash(data: str) -> tuple[str, str]:
    """Splits a stored string into salt and hash.

    Example:
        ```python
        >>> salt, hash_ = deserialize_hash("abcdef1234$9876543210")
        >>> isinstance(salt, str)
        True
        >>> isinstance(hash_, str)
        True
        ```
    """
    salt_hex, hash_hex = data.split("$")
    return salt_hex, hash_hex
