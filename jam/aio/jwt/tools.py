# -*- coding: utf-8 -*-

from asyncio import to_thread
from typing import Any, Optional

from jam.jwt.tools import __gen_jwt__, __payload_maker__, __validate_jwt__


async def __gen_jwt_async__(
    header: dict[str, Any],
    payload: dict[str, Any],
    secret: Optional[str] = None,
    private_key: Optional[str] = None,
) -> str:
    """Method for generating JWT token with different algorithms.

    Example:
    ```python
    token = await __gen_jwt_async__(
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
    return await to_thread(__gen_jwt__, header, payload, secret, private_key)


async def __validate_jwt_async__(
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
    return await to_thread(
        __validate_jwt__, token, check_exp, secret, public_key
    )


async def __payload_maker_async__(
    exp: Optional[int] = None, **data: Any
) -> dict[str, Any]:
    """Tool for making base payload.

    Args:
        exp (int | None): Token expire
        **data: Data for payload

    Returns:
        (dict[str, Any])
    """
    return await to_thread(__payload_maker__, exp, **data)
