# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
import logging
from typing import Literal

from jam.config import JAMConfig
from jam.jwt.__dev_tools__ import __gen_access_token__, __gen_refresh_token__
from jam.jwt.__errors__ import JamInvalidSignature as InvalidSignature
from jam.jwt.__errors__ import JamJWTMakingError as JWTError
from jam.jwt.__errors__ import JamNullJWTSecret as NullSecret
from jam.jwt.types import Tokens


def gen_jwt_tokens(*, config: JAMConfig, payload: dict = {}) -> Tokens:
    """
    Service for generating JWT tokens

    Example:
    ```python
    config = JAMConfig(
        JWT_ACCESS_SECRET_KEY="SOME_SUPER_SECRET_KEY",
        JWT_REFRESH_SECRET_KEY="ANOTHER_SECRET_KEY"
    )

    payload: dict = {
        "id": 1,
        "username": "lyaguxafrog"
    }

    tokens = gen_jwt_tokens(config=config, payload=payload)
    access_token: str = tokens.access
    refresh_token: str = tokens.refresh
    ```

    :param config: Standart jam config
    :type config: jam.config.JAMConfig
    :param payload: Custom user payload
    :type payload: dict

    :returns: Base model with access and refresh tokens
    :rtype: jam.jwt.types.Tokens
    """

    try:
        access: str = __gen_access_token__(config, payload)
        refresh: str = __gen_refresh_token__(config, payload)

    except Exception as e:
        raise JWTError(message=e)

    return Tokens(access=access, refresh=refresh)


def check_jwt_signature(
    *, config: JAMConfig, token_type: Literal["access", "refresh"], token: str
) -> bool:
    """
    Service for checking JWT signature

    :param config: Base jam config
    :type config: jam.config.JAMConfig
    :param token: JWT token
    :type token: str
    :param key_type: Type of JWT ( access token or refresh token )
    :type key_type: str

    :returns: Bool with signature status
    :rtype: bool
    """

    if token_type == "access":
        secret_key: str | None = config.JWT_ACCESS_SECRET_KEY

    elif token_type == "refresh":
        secret_key: str | None = config.JWT_REFRESH_SECRET_KEY

    else:
        raise ValueError("Invalid key type. Must be 'access' or 'refresh'.")

    if not secret_key:
        raise NullSecret("The specified secret key is missing.")

    try:
        header, payload, signature = token.split(".")
    except ValueError:
        raise ValueError(
            "Invalid token format. Token must have three parts separated by '.'"
        )

    data_to_sign = f"{header}.{payload}".encode("utf-8")

    expected_signature = (
        base64.urlsafe_b64encode(
            hmac.new(
                secret_key.encode("utf-8"), data_to_sign, hashlib.sha256
            ).digest()
        )
        .decode("utf-8")
        .rstrip("=")
    )

    return expected_signature == signature


def decode_token(
    *,
    config: JAMConfig,
    token: str,
    checksum: bool = False,
    checksum_token_type: Literal["access", "refresh"] | None = None,
) -> dict:
    """
    Service for decoding JWT token

    :param config: Base jam config
    :type config: jam.config.JAMConfig
    :param token: Some jwt token
    :type token: str
    :param checksum: Use `check_jwt_signature` in decode?
    :type checksum: bool
    :param checksum_token_type: Type of JWT ( access or refresh )
    :type checksum_token_type: str | None

    :retutns: Dict with information in token
    :rtype: dict
    """

    if checksum:
        sum: bool = check_jwt_signature(
            config=config, token_type=checksum_token_type, token=token  # type: ignore
        )
        if not sum:
            raise InvalidSignature
        else:
            logging.info("Signature valid")
            pass
    else:
        pass

    if not config.JWT_ACCESS_SECRET_KEY or not config.JWT_REFRESH_SECRET_KEY:
        raise NullSecret

    try:
        header, payload, signature = token.split(".")
    except ValueError:
        raise ValueError(
            "Invalid token format. Token must have three parts separated by '.'"
        )

    try:
        padding: str = "=" * (4 - len(payload) % 4)
        decoded_payload: bytes = base64.urlsafe_b64decode(payload + padding)
        return json.loads(decoded_payload)
    except (ValueError, json.JSONDecodeError) as e:
        raise ValueError("Failed to decode the payload: " + str(e))
