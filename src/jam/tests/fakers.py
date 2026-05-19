# -*- coding: utf-8 -*-

import json
from secrets import token_urlsafe
from typing import Any
import uuid

from jam.__deprecated__ import deprecated
from jam.jose.utils import __base64url_encode__ as base64url_encode
from jam.utils import xor_my_data


@deprecated("Use fake_jwt_token_v2")
def fake_jwt_token(payload: dict[str, Any] | None) -> str:
    """Generate a fake JWT token for testing purposes.

    !!! Deprecated
            Use fake_jwt_token_v2 instead.

    Returns:
        str: A fake JWT token.
    """
    header = {"typ": "fake-JWT", "alg": "none"}
    payload_data = payload or {}

    header_b64 = base64url_encode(
        json.dumps(header, separators=(",", ": ")).encode("utf-8")
    )
    payload_b64 = base64url_encode(
        json.dumps(payload_data, separators=(",", ": ")).encode("utf-8")
    )
    signature = "fake_signature"

    return f"{header_b64}.{payload_b64}.{signature}"


def fake_jwt_token_v2(
    iss: str | None = None,
    sub: str | None = None,
    aud: str | None = None,
    exp: int | None = None,
    nbf: int | None = None,
    jti: str | None = None,
    payload: dict[str, Any] | None = None,
    header: dict[str, Any] | None = None,
) -> str:
    """Generate a fake JWT token for testing purposes."""
    _header = {"typ": "fake-JWT", "alg": "fake-alg"}
    _header.update(header or {})
    payload = {
        "iss": iss,
        "sub": sub,
        "aud": aud,
        "exp": exp,
        "nbf": nbf,
        "jti": jti,
        **(payload or {}),
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    header_64 = base64url_encode(json.dumps(_header).encode("utf-8"))
    payload_64 = base64url_encode(json.dumps(payload).encode("utf-8"))

    return f"{header_64}.{payload_64}.fake_signature"


def invalid_token() -> str:
    """Generate an invalid JWT token for testing purposes.

    Returns:
        str: An invalid JWT token.
    """
    return f"INVALID_{token_urlsafe(16)}_TOKEN"


def fake_oauth2_token() -> str:
    """Return VALID fake oauth2 token."""
    k = "JAM_FAKE"
    token = f"VALID_OAUTH2_TOKEN:{token_urlsafe(4)}"
    return xor_my_data(token, k)


def invalid_oauth2_token() -> str:
    """Invalid OAuth2 token."""
    k = "JAM_FAKE"
    token = f"INVALID_OAUTH2_TOKEN:{token_urlsafe(4)}"
    return xor_my_data(token, k)


def generate_session_id() -> str:
    """Generate a unique session ID for testing purposes.

    Returns:
        str: A unique session ID.
    """
    return f"fake-session-{uuid.uuid4().hex}"


def fake_paseto_token(
    payload: dict[str, Any] | None = None,
    footer: dict[str, Any] | str | bytes | None = None,
) -> str:
    """Generate a fake PASETO token for testing purposes.

    This token ALWAYS validates successfully when decoded.

    Args:
        payload (dict[str, Any] | None): Payload to include in the PASETO token.
        footer (dict[str, Any] | str | bytes | None): Footer for the PASETO token.

    Returns:
        str: A fake PASETO token.
    """
    version = "v_fake"
    purpose = "local"
    payload_data = payload or {}

    payload_json = json.dumps(payload_data, separators=(",", ": "))
    payload_b64 = base64url_encode(payload_json.encode("utf-8"))

    token = f"{version}.{purpose}.{payload_b64}"

    if footer:
        if isinstance(footer, dict):
            footer_json = json.dumps(footer, separators=(",", ": "))
            footer_b64 = base64url_encode(footer_json.encode("utf-8"))
        elif isinstance(footer, bytes):
            footer_b64 = base64url_encode(footer)
        else:
            footer_b64 = base64url_encode(str(footer).encode("utf-8"))
        token += f".{footer_b64}"

    return token


def fake_jws_token(
    data: dict[str, Any] | str | None = None,
    header: dict[str, Any] | None = None,
) -> str:
    """Generate a fake JWS token for testing purposes.

    Args:
        data (dict[str, Any] | str | None): Data to sign.
        header (dict[str, Any] | None): JWS header.

    Returns:
        str: A fake JWS token.
    """
    _header = {"typ": "fake-JWS", "alg": "none"}
    _header.update(header or {})

    if isinstance(data, dict):
        payload = json.dumps(data)
    else:
        payload = data or "fake_data"

    header_b64 = base64url_encode(json.dumps(_header).encode("utf-8"))
    payload_b64 = base64url_encode(payload.encode("utf-8"))

    return f"{header_b64}.{payload_b64}.fake_signature"


def fake_jwe_token(
    data: dict[str, Any] | str | None = None,
    header: dict[str, Any] | None = None,
) -> str:
    """Generate a fake JWE token for testing purposes.

    Args:
        data (dict[str, Any] | str | None): Data to encrypt.
        header (dict[str, Any] | None): JWE header.

    Returns:
        str: A fake JWE token.
    """
    _header = {"typ": "fake-JWE", "alg": "fake-alg", "enc": "fake-enc"}
    _header.update(header or {})

    if isinstance(data, dict):
        payload = json.dumps(data)
    else:
        payload = data or "fake_encrypted_data"

    header_b64 = base64url_encode(json.dumps(_header).encode("utf-8"))
    payload_b64 = base64url_encode(payload.encode("utf-8"))

    return f"{header_b64}.{payload_b64}.fake_encrypted.fake_signature"
