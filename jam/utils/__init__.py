# -*- coding: utf-8 -*-

"""Various utilities that help with authorization."""

from .aes import generate_aes_key
from .otp_keys import generate_otp_key
from .rsa import generate_rsa_key_pair
from .salt_hash import (
    check_password,
    deserialize_hash,
    hash_password,
    serialize_hash,
)
from .xor import xor_my_data
