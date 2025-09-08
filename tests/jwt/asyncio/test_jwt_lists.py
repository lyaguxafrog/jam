# -*- coding: utf-8 -*-

from threading import Thread

import pytest
from fakeredis import FakeAsyncRedis, FakeRedis
from pytest import fixture, raises
from tinydb import TinyDB

from jam.aio import Jam
from jam.aio.jwt.lists.json import JSONList
from jam.aio.jwt.lists.redis import RedisList
from jam.exceptions import TokenInBlackList, TokenNotInWhiteList


t = TinyDB(":memory:")
t.truncate()


@fixture(scope="function")
def fake_aioredis() -> FakeAsyncRedis:
    """Mock redis instance."""
    return FakeAsyncRedis()


@fixture(scope="function")
def redis_black_list(fake_aioredis):
    return RedisList(
        type="black", redis_uri=fake_aioredis, in_list_life_time=None
    )


@fixture(scope="function")
def redis_white_list(fake_aioredis):
    return RedisList(
        type="white", redis_uri=fake_aioredis, in_list_life_time=None
    )


@fixture(scope="function")
def json_black_list():
    return JSONList(type="black", json_path=":memory:")


@fixture(scope="function")
def json_white_list():
    return JSONList(type="white", json_path=":memory:")


def test_redis_list_init(fake_aioredis):
    list = RedisList(
        type="black", redis_uri=fake_aioredis, in_list_life_time=10
    )

    assert list.__list_type__ == "black"


@pytest.mark.asyncio
async def test_redis_black_lists(fake_aioredis):
    config = {
        "auth_type": "jwt",
        "alg": "HS256",
        "secret_key": "secret",
        "list": {
            "type": "black",
            "backend": "redis",
            "redis_uri": fake_aioredis,
            "in_list_life_time": 3600,
        },
    }

    jam = Jam(config=config)

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
async def test_redis_white_lists(fake_aioredis):
    config = {
        "auth_type": "jwt",
        "alg": "HS256",
        "secret_key": "secret",
        "list": {
            "type": "white",
            "backend": "redis",
            "redis_uri": fake_aioredis,
            "in_list_life_time": 3600,
        },
    }

    jam = Jam(config=config)
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
    config = {
        "auth_type": "jwt",
        "alg": "HS256",
        "secret_key": "secret",
        "list": {
            "type": "black",
            "backend": "json",
            "json_path": ":memory:",
        },
    }
    jam = Jam(config=config)
    payload = {"json_list": "penis"}

    token = await jam.gen_jwt_token(payload)
    _payload = await jam.verify_jwt_token(
        token, check_exp=False, check_list=True
    )

    assert payload == _payload

    await jam.module.list.add(token)

    with raises(TokenInBlackList):
        await jam.verify_jwt_token(token, check_list=True, check_exp=False)

    await jam.module.list.delete(token)
    t.truncate()


@pytest.mark.asyncio
async def test_json_white_lists(json_white_list):
    config = {
        "auth_type": "jwt",
        "alg": "HS256",
        "secret_key": "secret",
        "list": {
            "type": "white",
            "backend": "json",
            "json_path": ":memory:",
        },
    }

    jam = Jam(config=config)
    payload = {"user_id": 1100}

    token = await jam.gen_jwt_token(payload)

    _payload = await jam.verify_jwt_token(
        token, check_exp=False, check_list=True
    )
    assert _payload == payload

    await jam.module.list.delete(token)
    with raises(TokenNotInWhiteList):
        await jam.verify_jwt_token(token, check_exp=False, check_list=True)

    t.truncate()
