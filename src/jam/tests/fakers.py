# -*- coding: utf-8 -*-

import json
from secrets import token_urlsafe
from typing import Any
import uuid

from jam.jwt.utils import base64url_encode
from jam.utils import xor_my_data


def fake_jwt_token(payload: dict[str, Any] | None) -> str:
    """Generate a fake JWT token for testing purposes.

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


def invalid_token() -> str:
    """Generate an invalid JWT token for testing purposes.

    Returns:
        str: An invalid JWT token.
    """
    return "INVALID_TOKEN"


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
    version = "v4"
    purpose = "local"
    payload_data = payload or {}

    payload_json = json.dumps(payload_data, separators=(",", ": "))
    payload_b64 = base64url_encode(payload_json.encode("utf-8")).decode("utf-8")

    token = f"{version}.{purpose}.{payload_b64}"

    if footer:
        if isinstance(footer, dict):
            footer_json = json.dumps(footer, separators=(",", ": "))
            footer_b64 = base64url_encode(footer_json.encode("utf-8")).decode(
                "utf-8"
            )
        elif isinstance(footer, bytes):
            footer_b64 = base64url_encode(footer).decode("utf-8")
        else:
            footer_b64 = base64url_encode(str(footer).encode("utf-8")).decode(
                "utf-8"
            )
        token += f".{footer_b64}"

    return token
