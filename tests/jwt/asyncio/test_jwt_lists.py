# -*- coding: utf-8 -*-
import pytest
from fakeredis import FakeAsyncRedis
from pytest import fixture, raises

from jam.asyncio import Jam
from jam.asyncio.jwt.lists.json import JSONList
from jam.asyncio.jwt.lists.redis import RedisList
from jam.exceptions import TokenInBlackList, TokenNotInWhiteList
from jam.utils import make_jwt_config


@fixture(scope="function")
def fake_aioredis() -> FakeAsyncRedis:
    """Mock redis instance."""
    return FakeAsyncRedis()


@fixture(scope="function")
def redis_black_list(fake_aioredis):
    return RedisList(
        type="black", redis_instance=fake_aioredis, in_list_life_time=None
    )


@fixture(scope="function")
def redis_white_list(fake_aioredis):
    return RedisList(
        type="white", redis_instance=fake_aioredis, in_list_life_time=None
    )


@fixture(scope="function")
def json_black_list():
    return JSONList(type="black", json_path="json-for-tests.json")


@fixture(scope="function")
def json_white_list():
    return JSONList(type="white", json_path="json-for-tests.json")


def test_redis_list_init(fake_aioredis):
    list = RedisList(
        type="black", redis_instance=fake_aioredis, in_list_life_time=10
    )

    assert list.__list_type__ == "black"


@pytest.mark.asyncio
async def test_redis_black_lists(redis_black_list):
    config = make_jwt_config(
        alg="HS256", secret_key="secret", list=redis_black_list
    )

    jam = Jam(auth_type="jwt", config=config)

    payload = {"token": 1}

    # verify new token
    token = await jam.gen_jwt_token(payload)
    _payload = await jam.verify_jwt_token(
        token, check_exp=False, check_list=True
    )

    assert payload == _payload

    # check blacklist
    await jam.module.list.add(token)

    with raises(TokenInBlackList):
        __payload = await jam.verify_jwt_token(
            token=token, check_exp=False, check_list=True
        )


@pytest.mark.asyncio
async def test_redis_white_lists(redis_white_list):
    config = make_jwt_config(
        alg="HS512", secret_key="secret", list=redis_white_list
    )

    jam = Jam(auth_type="jwt", config=config)
    payload = {"user_id": 1}

    token = await jam.gen_jwt_token(payload)

    _payload = await jam.verify_jwt_token(
        token, check_exp=False, check_list=True
    )
    assert _payload == payload

    await jam.module.list.delete(token)
    with raises(TokenNotInWhiteList):
        await jam.verify_jwt_token(token, check_exp=False, check_list=True)


@pytest.mark.asyncio
async def test_json_black_lists(json_black_list):
    config = make_jwt_config(
        alg="HS384", secret_key="secret", list=json_black_list
    )
    jam = Jam(auth_type="jwt", config=config)
    payload = {"json_list": "penis"}

    token = await jam.gen_jwt_token(payload)
    _payload = await jam.verify_jwt_token(
        token, check_exp=False, check_list=True
    )

    assert payload == _payload

    await jam.module.list.add(token)

    with raises(TokenInBlackList):
        await jam.verify_jwt_token(token, check_list=True, check_exp=False)


@pytest.mark.asyncio
async def test_json_white_lists(json_white_list):
    config = make_jwt_config(
        alg="HS512", secret_key="secret", list=json_white_list
    )

    jam = Jam(auth_type="jwt", config=config)
    payload = {"user_id": 1100}

    token = await jam.gen_jwt_token(payload)

    _payload = await jam.verify_jwt_token(
        token, check_exp=False, check_list=True
    )
    assert _payload == payload

    await jam.module.list.delete(token)
    with raises(TokenNotInWhiteList):
        await jam.verify_jwt_token(token, check_exp=False, check_list=True)
