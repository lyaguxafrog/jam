# -*- coding: utf-8 -*-

import hashlib
import hmac
import json
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from jam.exceptions import (
    EmptyPublicKey,
    EmptySecretKey,
    EmtpyPrivateKey,
    NotFoundSomeInPayload,
    TokenLifeTimeExpired,
)
from jam.jwt.__utils__ import __base64url_decode__, __base64url_encode__


def __gen_jwt__(
    header: dict[str, Any],
    payload: dict[str, Any],
    secret: Optional[str] = None,
    private_key: Optional[str] = None,
) -> str:
    """Method for generating JWT token with different algorithms.

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
        header (dict[str, str]): Dict with JWT headers
        payload (dict[str, Any]): Custom JWT payload
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

    signature_input = f"{header_encoded}.{payload_encoded}".encode()

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


def __validate_jwt__(
    token: str,
    check_exp: bool = False,
    secret: Optional[str] = None,
    public_key: Optional[str] = None,
) -> dict[str, Any]:
    """Validate a JWT token and return the payload if valid.

    Args:
        token (str): The JWT token to validate.
        check_exp (bool): true to check token lifetime.
        secret (str | None): Secret key for HMAC algorithms.
        public_key (str | None): Public key for RSA algorithms.

    Returns:
        (dict[str, Any]): The payload if the token is valid.

    Raises:
        ValueError: If the token is invalid.
        EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None.
        EmtpyPublicKey: If RSA algorithm is selected, but public key None.
        NotFoundSomeInPayload: If 'exp' not found in payload.
        TokenLifeTimeExpired: If token has expired.
    """
    try:
        header_encoded, payload_encoded, signature_encoded = token.split(".")
    except ValueError:
        raise ValueError("Invalid token format")

    header = json.loads(__base64url_decode__(header_encoded).decode("utf-8"))
    payload = json.loads(__base64url_decode__(payload_encoded).decode("utf-8"))
    signature = __base64url_decode__(signature_encoded)

    signature_input = f"{header_encoded}.{payload_encoded}".encode()

    if header["alg"].startswith("HS"):
        if secret is None:
            raise EmptySecretKey
        expected_signature = hmac.new(
            secret.encode("utf-8"), signature_input, hashlib.sha256
        ).digest()
    elif header["alg"].startswith("RS"):
        if public_key is None:
            raise EmptyPublicKey
        rsa_key = RSA.import_key(public_key)
        hash_obj = SHA256.new(signature_input)
        try:
            pkcs1_15.new(rsa_key).verify(hash_obj, signature)
            expected_signature = signature
        except (ValueError, TypeError):
            raise ValueError("Invalid signature")
    else:
        raise ValueError("Unsupported algorithm")

    if expected_signature != signature:
        raise ValueError("Invalid token signature")

    if check_exp:
        if payload["exp"] is None:
            raise NotFoundSomeInPayload('"exp" not found in payload')
        if payload["exp"] < datetime.today().timestamp():
            raise TokenLifeTimeExpired

    return payload


def __payload_maker__(exp: Optional[int], **data) -> dict[str, Any]:
    """Tool for making base payload.

    Args:
        exp (int | None): Token expire
        **data: Data for payload

    Returns:
        (dict[str, Any])
    """
    base_payload: dict = {
        "iat": datetime.now().timestamp(),
        "exp": exp,
        "jti": str(uuid4()),
    }

    base_payload.update(data)
    return base_payload
