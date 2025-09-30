# -*- coding: utf-8 -*-

from typing import Any

from jam.jwt.tools import __gen_jwt__


def fake_jwt_token(payload: dict[str, Any] | None) -> str:
    """Generate a fake JWT token for testing purposes.

    Returns:
        str: A fake JWT token.
    """
    return __gen_jwt__(
        header={"alg": "HS256", "typ": "fake-JWT"},
        payload=(
            payload
            if payload
            else {"sub": "1234567890", "name": "JohnDoe", "iat": 1616239022}
        ),
        secret="FAKE",
    )


def invalid_token() -> str:
    """Generate an invalid JWT token for testing purposes.

    Returns:
        str: An invalid JWT token.
    """
    return __gen_jwt__(
        header={"alg": "HS256", "typ": "invalid-JWT"},
        payload={"sub": "0987654321", "name": "Jane Doe", "iat": 1616239022},
        secret="FAKE",
    )
