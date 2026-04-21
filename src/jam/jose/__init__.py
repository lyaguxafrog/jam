# -*- coding: utf-8 -*-

"""JOSE tools."""

from typing import Any

from jam.jose.jwk import JWK, JWKOct, JWKSet, JWKRSA, JWKEC
from jam.jose.jws import JWS
from jam.jose.jwe import JWE
from jam.jose.jwt import JWT
from jam.logger import BaseLogger, logger
from jam.encoders import BaseEncoder, JsonEncoder


def create_instance(
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
]