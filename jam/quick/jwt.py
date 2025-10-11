# -*- coding: utf-8 -*-

"""Quick JWT methods."""

from typing import Any, Optional

from jam.__deprecated__ import deprecated
from jam.aio.jwt.tools import __gen_jwt_async__, __validate_jwt_async__
from jam.exceptions import EmptyPublicKey, EmptySecretKey, EmtpyPrivateKey
from jam.jwt.tools import __gen_jwt__, __validate_jwt__


_DEPRECATED_MESSAGE: str = (
    "All `quick` methods are deprecated and will be removed in version 3.0.0+."
)


@deprecated(_DEPRECATED_MESSAGE)
def get_jwt_token(
    alg: str,
    payload: dict[str, Any],
    secret_key: Optional[str] = None,
    private_key: Optional[str] = None,
) -> str:
    """Quick method for generate JWT token.

    Args:
        alg (str): Jwt algorithm
        payload (dict[str, Any]): Payload with information
        secret_key (str | None): Secret key for HS algs
        private_key (str | None): Private key for RS algs

    Returns:
        (str): New jwt token

    Deprecated:
       All `quick` methods are deprecated and will be removed in version 3.0.0+.

    Raises:
        EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
        EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        ValueError: Unsupported alg
    """
    try:
        token = __gen_jwt__(
            header={"alg": alg, "typ": "jwt"},
            payload=payload,
            secret=secret_key,
            private_key=private_key,
        )
        return token
    except ValueError as e:
        raise ValueError(e)
    except EmptySecretKey as e:
        raise EmptySecretKey(e)
    except EmtpyPrivateKey as e:
        raise EmtpyPrivateKey(e)


@deprecated(_DEPRECATED_MESSAGE)
async def aget_jwt_token(
    alg: str,
    payload: dict[str, Any],
    secret_key: Optional[str] = None,
    private_key: Optional[str] = None,
) -> str:
    """Quick method for generate JWT token (async).

    Args:
        alg (str): Jwt algorithm
        payload (dict[str, Any]): Payload with information
        secret_key (str | None): Secret key for HS algs
        private_key (str | None): Private key for RS algs

    Returns:
        (str): New jwt token

    Deprecated:
       All `quick` methods are deprecated and will be removed in version 3.0.0+.

    Raises:
        EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
        EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        ValueError: Unsupported alg
    """
    try:
        token = await __gen_jwt_async__(
            header={"alg": alg, "typ": "jwt"},
            payload=payload,
            secret=secret_key,
            private_key=private_key,
        )
        return token
    except ValueError as e:
        raise ValueError(e)
    except EmptySecretKey as e:
        raise EmptySecretKey(e)
    except EmtpyPrivateKey as e:
        raise EmtpyPrivateKey(e)


@deprecated(_DEPRECATED_MESSAGE)
def verify_jwt_token(
    token: str,
    secret_key: Optional[str] = None,
    public_key: Optional[str] = None,
) -> bool:
    """Method to verify the token.

    Args:
        token (str): JWT token
        secret_key (str | None): Secret key for HS algs
        public_key (str | None): Public key for RS algs

    Returns:
        (bool): If token is valid

    Deprecated:
       All `quick` methods are deprecated and will be removed in version 3.0.0+.

    Raises:
        EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None.
        EmtpyPublicKey: If RSA algorithm is selected, but public key None.
    """
    try:
        __validate_jwt__(token=token, secret=secret_key, public_key=public_key)
    except EmptySecretKey as e:
        raise EmptySecretKey(e)
    except EmptyPublicKey as e:
        raise EmptyPublicKey(e)
    except ValueError:
        return False

    return True


@deprecated(_DEPRECATED_MESSAGE)
async def averify_jwt_token(
    token: str,
    secret_key: Optional[str] = None,
    public_key: Optional[str] = None,
) -> bool:
    """Method to verify the token (async).

    Args:
        token (str): JWT token
        secret_key (str | None): Secret key for HS algs
        public_key (str | None): Public key for RS algs

    Returns:
        (bool): If token is valid

    Deprecated:
       All `quick` methods are deprecated and will be removed in version 3.0.0+.

    Raises:
        EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None.
        EmtpyPublicKey: If RSA algorithm is selected, but public key None.
    """
    try:
        await __validate_jwt_async__(
            token=token, secret=secret_key, public_key=public_key
        )
    except EmptySecretKey as e:
        raise EmptySecretKey(e)
    except EmptyPublicKey as e:
        raise EmptyPublicKey(e)
    except ValueError:
        return False

    return True


@deprecated(_DEPRECATED_MESSAGE)
def decode_jwt_token(
    token: str,
    secret_key: Optional[str] = None,
    public_key: Optional[str] = None,
) -> dict[str, Any]:
    """Token decoding.

    Args:
        token (str): JWT token
        secret_key (str | None): Secret key for HS algs
        public_key (str | None): Public key for RS algs

    Returns:
        (dict[str, Any]): Decoded payload

    Deprecated:
       All `quick` methods are deprecated and will be removed in version 3.0.0+.

    Raises:
        ValueError: If the token is invalid.
        EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None.
        EmtpyPublicKey: If RSA algorithm is selected, but public key None.
    """
    try:
        payload = __validate_jwt__(
            token=token, secret=secret_key, public_key=public_key
        )
        return payload
    except ValueError as e:
        raise ValueError(e)
    except EmptyPublicKey as e:
        raise EmptyPublicKey(e)
    except EmptySecretKey as e:
        raise EmptySecretKey(e)


@deprecated(_DEPRECATED_MESSAGE)
async def adecode_jwt_token(
    token: str,
    secret_key: Optional[str] = None,
    public_key: Optional[str] = None,
) -> dict[str, Any]:
    """Token decoding (async).

    Args:
        token (str): JWT token
        secret_key (str | None): Secret key for HS algs
        public_key (str | None): Public key for RS algs

    Returns:
        (dict[str, Any]): Decoded payload

    Deprecated:
       All `quick` methods are deprecated and will be removed in version 3.0.0+.

    Raises:
        ValueError: If the token is invalid.
        EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None.
        EmtpyPublicKey: If RSA algorithm is selected, but public key None.
    """
    try:
        payload = await __validate_jwt_async__(
            token=token, secret=secret_key, public_key=public_key
        )
        return payload
    except ValueError as e:
        raise ValueError(e)
    except EmptyPublicKey as e:
        raise EmptyPublicKey(e)
    except EmptySecretKey as e:
        raise EmptySecretKey(e)
