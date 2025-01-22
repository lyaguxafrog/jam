# -*- coding: utf-8 -*-

"""
Only private tools in JAM JWT
"""

import base64
import hashlib
import hmac
import json
import secrets
import time

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


def __gen_access_token__(config: JAMConfig, payload: dict) -> str:
    """
    Private tool for generating access token

    :param config: Standart jam confg
    :type config: jam.config.JAMConfig
    :param payload: Custom user payload
    :type payload: dict

    :returns: Returns access token by string
    :rtype: str
    """

    if not config.JWT_ACCESS_SECRET_KEY:
        raise NullSecret(message="JWT_ACCESS_SECRET_KEY is null")

    __payload__: dict = {
        "data": payload,
        "exp": int(time.time()) + config.JWT_ACCESS_EXP,
    }

    encoded_header: str = __encode_base64__(
        json.dumps({"alg": config.JWT_ALGORITHM, "typ": "JWT"}).encode()
    )
    encoded_payload: str = __encode_base64__(json.dumps(__payload__).encode())

    __signature__: bytes = hmac.new(
        config.JWT_ACCESS_SECRET_KEY.encode(),
        f"{encoded_header}.{encoded_payload}".encode(),
        hashlib.sha256,
    ).digest()

    encoded_signature: str = __encode_base64__(__signature__)

    access_token: str = (
        f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    )
    return access_token


def __gen_refresh_token__(config: JAMConfig, payload: dict) -> str:
    """
    Private tool for generating refresh token

    :param config: Standart jam config
    :type config: jam.config.JAMConfig
    :param payload: Custom user payload
    :type payload: dict

    :returns: Returns refresh roken by string
    :type: str
    """

    if not config.JWT_REFRESH_SECRET_KEY:
        raise NullSecret(message="JWT_REFRESH_SECRET_KEY is null")

    __payload__: dict = {
        "data": payload,
        "exp": int(time.time()) + config.JWT_REFRESH_EXP,
        "jti": secrets.token_hex(16),
    }

    encoded_header: str = __encode_base64__(
        json.dumps({"alg": config.JWT_ALGORITHM, "typ": "JWT"}).encode()
    )
    encoded_payload: str = __encode_base64__(json.dumps(__payload__).encode())

    __signature__: bytes = hmac.new(
        config.JWT_REFRESH_SECRET_KEY.encode(),
        f"{encoded_header}.{encoded_payload}".encode(),
        hashlib.sha256,
    ).digest()

    encoded_signature: str = __encode_base64__(__signature__)

    refresh_token: str = (
        f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    )
    return refresh_token
