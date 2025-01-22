# -*- coding: utf-8 -*-

"""
Only private tools in JAM JWT
"""

import base64

from jam.config import JAMConfig
from jam.jwt.__errors__ import JamNullJWTSecret as NullSecret


def __check_secrets__(config: JAMConfig) -> bool:
    """
    Private tool for check secrets in confg

    :param config: Base jam config
    :type config: jam.config.JAMConfig

    :returns: True if secrets in config
    :rtype: bool
    """

    if not config.JWT_ACCESS_SECRET_KEY or not config.JWT_REFRESH_SECRET_KEY:
        raise NullSecret

    else:
        return True


def __encode_base64__(data: bytes) -> str:
    """
    Private helper function to encode data to base64 URL-safe format

    :param data: Bytes data
    :type data: bytes

    :returns: Encoded string
    :rtype: str
    """

    return base64.urlsafe_b64encode(data).decode().rstrip("=")
