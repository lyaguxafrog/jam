# -*- coding: utf-8 -*-

from fakeredis import FakeRedis
from pytest import fixture, raises
from tinydb import TinyDB

from jam import Jam
from jam.exceptions import TokenInBlackList, TokenNotInWhiteList
from jam.jwt.lists.json import JSONList
from jam.jwt.lists.redis import RedisList


t = TinyDB(":memory:")
t.truncate()


@fixture(scope="function")
def fake_redis() -> FakeRedis:
    """Mock redis instance."""
    return FakeRedis()


@fixture(scope="function")
def redis_black_list(fake_redis):
    return RedisList(type="black", redis_uri=fake_redis, in_list_life_time=None)


@fixture(scope="function")
def redis_white_list(fake_redis):
    return RedisList(type="white", redis_uri=fake_redis, in_list_life_time=None)


@fixture(scope="function")
def json_black_list():
    return JSONList(type="black", json_path=":memory:")


@fixture(scope="function")
def json_white_list():
    return JSONList(type="white", json_path=":memory:")


def test_redis_list_init(fake_redis):
    list = RedisList(type="black", redis_uri=fake_redis, in_list_life_time=10)

    assert list.__list_type__ == "black"


def test_redis_black_lists(fake_redis):
    config = {
        "jwt": {
            "alg": "HS256",
            "secret_key": "secret",
            "list": {
                "type": "black",
                "backend": "redis",
                "redis_uri": fake_redis,
                "in_list_life_time": 3600,
            },
        }
    }

    jam = Jam(config=config)

    payload = {"token": 1}

    # verify new token
    token = jam.gen_jwt_token(payload)
    _payload = jam.verify_jwt_token(token, check_exp=False, check_list=True)

    assert payload == _payload

    # check blacklist
    jam.jwt.list.add(token)

    with raises(TokenInBlackList):
        __payload = jam.verify_jwt_token(
            token=token, check_exp=False, check_list=True
        )


def test_redis_white_lists(fake_redis):
    config = {
        "jwt": {
            "alg": "HS256",
            "secret_key": "secret",
            "list": {
                "type": "white",
                "backend": "redis",
                "redis_uri": fake_redis,
                "in_list_life_time": 3600,
            },
        }
    }

    jam = Jam(config=config)
    payload = {"user_id": 1}

    token = jam.gen_jwt_token(payload)

    _payload = jam.verify_jwt_token(token, check_exp=False, check_list=True)
    assert _payload == payload

    jam.jwt.list.delete(token)
    with raises(TokenNotInWhiteList):
        jam.verify_jwt_token(token, check_exp=False, check_list=True)


def test_json_black_lists(json_black_list):
    config = {
        "jwt": {
            "alg": "HS256",
            "secret_key": "secret",
            "list": {
                "type": "black",
                "backend": "json",
                "json_path": ":memory:",
            },
        }
    }
    jam = Jam(config=config)
    payload = {"json_list": "penis"}

    token = jam.gen_jwt_token(payload)
    _payload = jam.verify_jwt_token(token, check_exp=False, check_list=True)

    assert payload == _payload

    jam.jwt.list.add(token)

    with raises(TokenInBlackList):
        jam.verify_jwt_token(token, check_list=True, check_exp=False)

    jam.jwt.list.delete(token)
    t.truncate()


def test_json_white_lists(json_white_list):
    config = {
        "jwt": {
            "alg": "HS256",
            "secret_key": "secret",
            "list": {
                "type": "white",
                "backend": "json",
                "json_path": ":memory:",
            },
        }
    }

    jam = Jam(config=config)
    payload = {"user_id": 1100}

    token = jam.gen_jwt_token(payload)

    _payload = jam.verify_jwt_token(token, check_exp=False, check_list=True)
    assert _payload == payload

    jam.jwt.list.delete(token)
    with raises(TokenNotInWhiteList):
        jam.verify_jwt_token(token, check_exp=False, check_list=True)
    t.truncate()
