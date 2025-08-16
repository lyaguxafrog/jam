# -*- coding: utf-8 -*-

"""Quick JWT methods."""

from typing import Any

from jam.asyncio.jwt.tools import __gen_jwt_async__, __validate_jwt_async__
from jam.exceptions import EmptyPublicKey, EmptySecretKey, EmtpyPrivateKey
from jam.jwt.tools import __gen_jwt__, __validate_jwt__


def get_jwt_token(
    alg: str,
    payload: dict[str, Any],
    secret_key: str | None = None,
    private_key: str | None = None,
) -> str:
    """Quick method for generate JWT token.

    Args:
        alg (str): Jwt algorithm
        payload (dict[str, Any]): Payload with information
        secret_key (str | None): Secret key for HS algs
        private_key (str | None): Private key for RS algs

    Returns:
        (str): New jwt token

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


async def aget_jwt_token(
    alg: str,
    payload: dict[str, Any],
    secret_key: str | None = None,
    private_key: str | None = None,
) -> str:
    """Quick method for generate JWT token (async).

    Args:
        alg (str): Jwt algorithm
        payload (dict[str, Any]): Payload with information
        secret_key (str | None): Secret key for HS algs
        private_key (str | None): Private key for RS algs

    Returns:
        (str): New jwt token

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


def verify_jwt_token(
    token: str, secret_key: str | None = None, public_key: str | None = None
) -> bool:
    """Method to verify the token.

    Args:
        token (str): JWT token
        secret_key (str | None): Secret key for HS algs
        public_key (str | None): Public key for RS algs

    Returns:
        (bool): If token is valid

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


async def averify_jwt_token(
    token: str, secret_key: str | None = None, public_key: str | None = None
) -> bool:
    """Method to verify the token (async).

    Args:
        token (str): JWT token
        secret_key (str | None): Secret key for HS algs
        public_key (str | None): Public key for RS algs

    Returns:
        (bool): If token is valid

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


def decode_jwt_token(
    token: str, secret_key: str | None = None, public_key: str | None = None
) -> dict[str, Any]:
    """Token decoding.

    Args:
        token (str): JWT token
        secret_key (str | None): Secret key for HS algs
        public_key (str | None): Public key for RS algs

    Returns:
        (dict[str, Any]): Decoded payload

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


async def adecode_jwt_token(
    token: str, secret_key: str | None = None, public_key: str | None = None
) -> dict[str, Any]:
    """Token decoding (async).

    Args:
        token (str): JWT token
        secret_key (str | None): Secret key for HS algs
        public_key (str | None): Public key for RS algs

    Returns:
        (dict[str, Any]): Decoded payload

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
