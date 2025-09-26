# -*- coding: utf-8 -*-

import pytest
from pytest_asyncio import fixture

from jam.aio.modules import JWTModule


@fixture
async def jwt_module_hs():
    return JWTModule(alg="HS256", secret_key="SECRET")


@fixture
async def jwt_module_rs():

    from jam.utils import generate_rsa_key_pair

    keys = generate_rsa_key_pair()

    return JWTModule(
        alg="RS256", private_key=keys["private"], public_key=keys["public"]
    )


@pytest.mark.asyncio
async def test_payload_maker(jwt_module_hs, jwt_module_rs):
    payload = await jwt_module_hs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )

    assert payload["jti"] is not None
    assert payload["user_id"] == 1
    assert payload["username"] == "test_user"

    payload = await jwt_module_rs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )

    assert payload["jti"] is not None
    assert payload["user_id"] == 1
    assert payload["username"] == "test_user"


@pytest.mark.asyncio
async def test_jwt_token_generation(jwt_module_hs, jwt_module_rs):

    from jam.jwt.tools import __validate_jwt__

    payload = await jwt_module_hs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )
    token = await jwt_module_hs.gen_token(payload=payload)
    assert token is not None
    assert isinstance(token, str)

    decoded_payload = __validate_jwt__(
        token=token,
        secret=jwt_module_hs._secret_key,
        check_exp=False,
        public_key=None,
    )

    assert decoded_payload["payload"] == payload

    payload = await jwt_module_rs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )
    token = await jwt_module_rs.gen_token(payload=payload)
    assert token is not None
    assert isinstance(token, str)

    decoded_payload = __validate_jwt__(
        token=token,
        secret=None,
        check_exp=False,
        public_key=jwt_module_rs.public_key,
    )

    assert decoded_payload["payload"] == payload


@pytest.mark.asyncio
async def test_jwt_token_validation(jwt_module_hs, jwt_module_rs):
    payload = await jwt_module_hs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )
    token = await jwt_module_hs.gen_token(payload=payload)
    assert token is not None
    assert isinstance(token, str)

    decoded_payload = (
        await jwt_module_hs.validate_payload(
            token=token, check_exp=False, check_list=False
        )
    )["payload"]
    assert decoded_payload == payload

    with pytest.raises(ValueError):
        await jwt_module_hs.validate_payload(
            token=token + "corrupted", check_exp=False, check_list=False
        )

    payload = await jwt_module_rs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )
    token = await jwt_module_rs.gen_token(payload=payload)
    assert token is not None
    assert isinstance(token, str)

    decoded_payload = (
        await jwt_module_rs.validate_payload(
            token=token, check_exp=False, check_list=False
        )
    )["payload"]
    assert decoded_payload == payload

    with pytest.raises(ValueError):
        await jwt_module_rs.validate_payload(
            token=token + "corrupted", check_exp=False, check_list=False
        )
