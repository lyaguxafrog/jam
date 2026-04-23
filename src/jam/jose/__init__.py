# -*- coding: utf-8 -*-

"""JOSE tools."""

from typing import Any

from jam.jose.jwk import JWK, JWKOct, JWKSet, JWKRSA, JWKEC
from jam.jose.jws import JWS
from jam.jose.jwe import JWE
from jam.jose.jwt import JWT
from jam.logger import BaseLogger, logger
from jam.encoders import BaseEncoder, JsonEncoder


def create_jwt_instance(
    alg: str,
    secret: Any = None,
    secret_key: Any = None,
    password: str | bytes | None = None,
    list: dict[str, Any] | None = None,
    logger: BaseLogger = logger,
    serializer: BaseEncoder | type[BaseEncoder] = JsonEncoder,
    **kwargs: Any,
) -> JWT:
    """Create JWT instance."""
    if secret is None and secret_key is not None:
        secret = secret_key
    elif secret is None:
        raise ValueError("Either 'secret' or 'secret_key' must be provided")

    key = secret
    if isinstance(secret, JWK):
        key = secret._to_keylike()

    return JWT(
        alg=alg,
        secret_key=key,
        password=password,
        list=list,
        serializer=serializer,
        logger=logger,
    )


def create_jws_instance(
    alg: str,
    key: Any = None,
    password: bytes | None = None,
    logger: BaseLogger = logger,
    **kwargs: Any,
) -> JWS:
    """Create JWS instance."""
    if key is None:
        raise ValueError("'key' must be provided")

    from jam.jose.jwk import JWK as JWKClass

    if isinstance(key, JWKClass):
        key = key._to_keylike()

    return JWS(
        alg=alg,
        key=key,
        password=password,
        logger=logger,
    )


def create_jwe_instance(
    alg: str,
    enc: str,
    key: Any = None,
    password: bytes | None = None,
    serializer: BaseEncoder | type[BaseEncoder] = JsonEncoder,
    logger: BaseLogger = logger,
    **kwargs: Any,
) -> JWE:
    """Create JWE instance."""
    if key is None:
        raise ValueError("'key' must be provided")

    from jam.jose.jwk import JWK as JWKClass

    if isinstance(key, JWKClass):
        key = key._to_keylike()

    return JWE(
        alg=alg,
        enc=enc,
        key=key,
        password=password,
        serializer=serializer,
        logger=logger,
    )


create_instance = create_jwt_instance


__all__ = [
    "JWK",
    "JWKSet",
    "JWS",
    "JWE",
    "JWT",
    "JWKRSA",
    "JWKEC",
    "JWKOct",
    "create_instance",
    "create_jwt_instance",
    "create_jws_instance",
    "create_jwe_instance",
]