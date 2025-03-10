# -*- coding: utf-8 -*-

import hashlib
import hmac
import json
from typing import Any, Dict

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from jam.exceptions import EmptySecretKey, EmtpyPrivateKey
from jam.jwt.__utils__ import __base64url_encode__


def __gen_jwt__(
    header: Dict[str, str],
    payload: Dict[str, Any],
    secret: str | None = None,
    private_key: str | None = None,
) -> str:
    """
    Method for generating JWT token with different algorithms

    Example:
    ```python
    token = __gen_jwt__(
        header={
            "alg": "HS256",
            "type": "jwt"
        },
        payload={
            "id": 1
        },
        secret="SUPER_SECRET"
    )
    ```

    Args:
        header (Dict[str, str]): Dict with JWT headers
        payload (Dict[str, Any]): Custom JWT payload
        secret (str | None): Secret key for HMAC algorithms
        private_key (str | None): Private key for RSA algorithms

    Raises:
        EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
        EmtpyPrivateKey: If RSA algorithm is selected, but private key None

    Returns:
        (str): Access/refresh token
    """
    header_encoded = __base64url_encode__(json.dumps(header).encode("utf-8"))
    payload_encoded = __base64url_encode__(json.dumps(payload).encode("utf-8"))

    signature_input = f"{header_encoded}.{payload_encoded}".encode("utf-8")

    if header["alg"].startswith("HS"):
        if secret is None:
            raise EmptySecretKey
        signature = hmac.new(
            secret.encode("utf-8"), signature_input, hashlib.sha256
        ).digest()
    elif header["alg"].startswith("RS"):
        if private_key is None:
            raise EmtpyPrivateKey
        rsa_key = RSA.import_key(private_key)
        hash_obj = SHA256.new(signature_input)
        signature = pkcs1_15.new(rsa_key).sign(hash_obj)
    else:
        raise ValueError("Unsupported algorithm")

    signature_encoded = __base64url_encode__(signature)

    jwt_token = f"{header_encoded}.{payload_encoded}.{signature_encoded}"
    return jwt_token
