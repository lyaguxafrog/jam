# -*- coding: utf-8 -*-

"""
Module for quick use of auth* without an instance.
"""

from .jwt import decode_jwt_token, get_jwt_token, verify_jwt_token


__all__ = ["get_jwt_token", "verify_jwt_token", "decode_jwt_token"]
