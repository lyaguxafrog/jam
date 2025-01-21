# -*- coding: utf-8 -*-

import base64
import json
import time

import pytest

from jam.config import JAMConfig
from jam.jwt.tools import (
    JWTError,
    NullSecret,
    __gen_access_token__,
    __gen_refresh_token__,
    gen_jwt_tokens,
)
from jam.jwt.types import Tokens


@pytest.fixture
def config() -> JAMConfig:
    """
    Fixture to create a JAMConfig configuration.

    :returns: JAMConfig object with specified parameters.
    :rtype: jam.config.JAMConfig
    """

    return JAMConfig(
        JWT_ACCESS_SECRET_KEY="SOME_SUPER_SECRET_KEY",
        JWT_REFRESH_SECRET_KEY="ANOTHER_SECRET_KEY",
        JWT_ACCESS_EXP=3600,  # 1 hour
        JWT_REFRESH_EXP=86400,  # 1 day
        JWT_ALGORITHM="HS256",
    )


def test_gen_access_token(config: JAMConfig) -> None:
    """
    Test for generating an access token.

    :param config: JAMConfig configuration.
    :type config: jam.config.JAMConfig
    """

    payload: dict = {"id": 1, "username": "testuser"}
    token: str = __gen_access_token__(config, payload)

    # Check that the token has 3 parts
    assert len(token.split(".")) == 3

    # Check that the token decodes and contains expected data
    header, encoded_payload, signature = token.split(".")
    decoded_payload = json.loads(
        base64.urlsafe_b64decode(encoded_payload + "==").decode()
    )
    assert decoded_payload["data"] == payload
    assert decoded_payload["exp"] > int(time.time())


def test_gen_refresh_token(config: JAMConfig) -> None:
    """
    Test for generating a refresh token.

    :param config: JAMConfig configuration.
    :type config: jam.config.JAMConfig
    """

    payload: dict = {"id": 1, "username": "testuser"}
    token: str = __gen_refresh_token__(config, payload)

    # Check that the token has 3 parts
    assert len(token.split(".")) == 3

    # Check that the token decodes and contains expected data
    header, encoded_payload, signature = token.split(".")
    decoded_payload = json.loads(
        base64.urlsafe_b64decode(encoded_payload + "==").decode()
    )
    assert decoded_payload["data"] == payload
    assert "jti" in decoded_payload
    assert decoded_payload["exp"] > int(time.time())


def test_gen_jwt_tokens(config: JAMConfig) -> None:
    """
    Test for generating JWT tokens.

    :param config: JAMConfig configuration.
    :type config: jam.config.JAMConfig
    """

    payload: dict = {"id": 1, "username": "testuser"}
    tokens: Tokens = gen_jwt_tokens(config=config, payload=payload)

    # Check that the returned object is Tokens with access and refresh tokens
    assert isinstance(tokens, Tokens)
    assert len(tokens.access.split(".")) == 3
    assert len(tokens.refresh.split(".")) == 3


def test_gen_access_token_no_secret(config: JAMConfig) -> None:
    """
    Test for handling missing secret key when generating access token.

    :param config: JAMConfig configuration.
    :type config: jam.config.JAMConfig
    """

    config.JWT_ACCESS_SECRET_KEY = None
    payload: dict = {"id": 1, "username": "testuser"}

    with pytest.raises(NullSecret):
        __gen_access_token__(config, payload)


def test_gen_refresh_token_no_secret(config: JAMConfig) -> None:
    """
    Test for handling missing secret key when generating refresh token.

    :param config: JAMConfig configuration.
    :type config: jam.config.JAMConfig
    """

    config.JWT_REFRESH_SECRET_KEY = None
    payload: dict = {"id": 1, "username": "testuser"}

    with pytest.raises(NullSecret):
        __gen_refresh_token__(config, payload)


def test_gen_jwt_tokens_error(config: JAMConfig) -> None:
    """
    Test for handling errors in token generation.

    :param config: JAMConfig configuration.
    :type config: jam.config.JAMConfig
    """

    config.JWT_ACCESS_SECRET_KEY = None

    with pytest.raises(JWTError):
        gen_jwt_tokens(config=config, payload={})
