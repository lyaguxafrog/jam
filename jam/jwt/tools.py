# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
import secrets
import time

from jam.config import JAMConfig
from jam.jwt.__errors__ import JamNullJWTSecret as NullSecret


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

    encoded_header: str = (
        base64.urlsafe_b64encode(
            json.dumps({"alg": config.JWT_ALGORITHM, "typ": "JWT"}).encode()
        )
        .decode()
        .rstrip("=")
    )
    encoded_payload: str = (
        base64.urlsafe_b64encode(json.dumps(__payload__).encode())
        .decode()
        .rstrip("=")
    )

    __signature__: bytes = hmac.new(
        config.JWT_ACCESS_SECRET_KEY.encode(),
        f"{encoded_header}.{encoded_payload}".encode(),
        hashlib.sha256,
    ).digest()
    encoded_signature: str = (
        base64.urlsafe_b64encode(__signature__).decode().rstrip("=")
    )

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
        raise NullSecret(message="JWT_REFRESH_TOKEN is null")

    __payload__: dict = {
        "data": payload,
        "exp": int(time.time()) + config.JWT_REFRESH_EXP,
        "jti": secrets.token_hex(16),
    }

    encoded_header: str = (
        base64.urlsafe_b64encode(
            json.dumps({"alg": config.JWT_ALGORITHM, "typ": "JWT"}).encode()
        )
        .decode()
        .rstrip("=")
    )
    encoded_payload: str = (
        base64.urlsafe_b64encode(json.dumps(__payload__).encode())
        .decode()
        .rstrip("=")
    )

    __signature__: bytes = hmac.new(
        config.JWT_REFRESH_SECRET_KEY.encode(),
        f"{encoded_header}.{encoded_payload}".encode(),
        hashlib.sha256,
    ).digest()
    encoded_signature: str = (
        base64.urlsafe_b64encode(__signature__).decode().rstrip("=")
    )

    refresh_token: str = (
        f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    )
    return refresh_token
