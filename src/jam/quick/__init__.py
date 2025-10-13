# -*- coding: utf-8 -*-

"""
Module for quick use of auth* without an instance.

This will be removed in the next major version.
"""

from .jwt import (
    adecode_jwt_token,
    aget_jwt_token,
    averify_jwt_token,
    decode_jwt_token,
    get_jwt_token,
    verify_jwt_token,
)


__all__ = [
    "aget_jwt_token",
    "averify_jwt_token",
    "adecode_jwt_token",
    "get_jwt_token",
    "verify_jwt_token",
    "decode_jwt_token",
]
