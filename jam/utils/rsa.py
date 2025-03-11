# -*- coding: utf-8 -*-

from cryptography.hazmat.primitives.asymmetric import rsa


def gen_keys(*, key_size: int = 2048, public_exponent: int = 65537):
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent, key_size=key_size
    )

    return private_key
