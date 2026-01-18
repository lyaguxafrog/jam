# -*- coding: utf-8 -*-

import json
from secrets import token_urlsafe
from typing import Any, Optional

from jam.jwt.utils import base64url_encode
from jam.utils import xor_my_data


def fake_jwt_token(payload: Optional[dict[str, Any]]) -> str:
    """Generate a fake JWT token for testing purposes.

    Returns:
        str: A fake JWT token.
    """
    header = {"typ": "fake-JWT", "alg": "none"}
    payload_data = payload or {}
    
    header_b64 = base64url_encode(json.dumps(header, separators=(",", ": ")).encode("utf-8"))
    payload_b64 = base64url_encode(json.dumps(payload_data, separators=(",", ": ")).encode("utf-8"))
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
