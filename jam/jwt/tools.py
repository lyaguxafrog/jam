# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
import secrets  # noqa
import time  # noqa

from jam.config import JAMConfig


def __gen_access_token__(config: JAMConfig, payload: dict) -> str:

    __payload__: dict = {"data": payload, "exp": config.JWT_ACCESS_EXP}

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
