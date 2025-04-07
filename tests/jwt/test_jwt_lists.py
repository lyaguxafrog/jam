# -*- coding: utf-8 -*-

from fakeredis import FakeRedis
from pytest import fixture, raises

from jam import Jam
from jam.exceptions import TokenInBlackList
from jam.jwt.lists import RedisList
from jam.utils import make_jwt_config


# @fixture(scope="function")
# def fake_redis() -> FakeRedis:
#     """Mock redis instance."""
#     return FakeRedis()


@fixture(scope="function")
def redis_black_list(fake_redis):
    return RedisList(
        type="black", redis_instance=fake_redis, in_list_life_time=None
    )


def test_redis_list_init(fake_redis):
    list = RedisList(
        type="black", redis_instance=fake_redis, in_list_life_time=10
    )

    assert list.__list_type__ == "black"


def test_redis_black_lists(redis_black_list):
    config = make_jwt_config(
        alg="HS256", secret_key="secret", list=redis_black_list
    )

    jam = Jam(auth_type="jwt", config=config)

    payload = {"token": 1}

    # verify new token
    token = jam.gen_jwt_token(payload)
    _payload = jam.verify_jwt_token(token, check_exp=False, check_list=True)

    assert payload == _payload

    # check blacklist

    jam.module.list.add(token)

    with raises(TokenInBlackList):
        __payload = jam.verify_jwt_token(
            token=token, check_exp=False, check_list=True
        )
