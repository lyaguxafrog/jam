# -*- coding: utf-8 -*-

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_rsa_key_pair(key_size: int = 2048) -> dict:
    """RSA key generation utility.

    Args:
        key_size (int): Size of RSA key

    Returns:
        (dict): with public and private keys in format:

    ```python
    {
        "public": "some_key",
        "private": "key"
    }
    ```
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=key_size, backend=default_backend()
    )

    public_key = private_key.public_key()

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return {
        "public": pem_public.decode("utf-8"),
        "private": pem_private.decode("utf-8"),
    }
