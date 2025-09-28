# -*- coding: utf-8 -*_

import pytest
from fakeredis import FakeRedis

from jam.modules import JWTModule


@pytest.fixture
def jwt_module_hs():
    return JWTModule(alg="HS256", secret_key="SECRET")


@pytest.fixture
def jwt_module_rs():

    from jam.utils import generate_rsa_key_pair

    keys = generate_rsa_key_pair()

    return JWTModule(
        alg="RS256", private_key=keys["private"], public_key=keys["public"]
    )


@pytest.fixture
def jwt_module_hs_redis_black_list():
    return JWTModule(
        alg="HS256",
        secret_key="SECRET",
        list={
            "backend": "redis",
            "type": "black",
            "redis_uri": FakeRedis(decode_responses=True),
            "in_list_life_time": 6000,
        },
    )


@pytest.fixture
def jwt_module_rs_redis_black_list():

    from jam.utils import generate_rsa_key_pair

    keys = generate_rsa_key_pair()

    return JWTModule(
        alg="RS256",
        public_key=keys["public"],
        private_key=keys["private"],
        list={
            "backend": "redis",
            "type": "black",
            "redis_uri": FakeRedis(decode_responses=True),
            "in_list_life_time": 6000,
        },
    )


@pytest.fixture
def jwt_module_hs_redis_white_list():
    return JWTModule(
        alg="HS256",
        secret_key="SECRET",
        list={
            "backend": "redis",
            "type": "white",
            "redis_uri": FakeRedis(decode_responses=True),
            "in_list_life_time": 6000,
        },
    )


@pytest.fixture
def jwt_module_rs_redis_white_list():
    from jam.utils import generate_rsa_key_pair

    keys = generate_rsa_key_pair()

    return JWTModule(
        alg="RS256",
        public_key=keys["public"],
        private_key=keys["private"],
        list={
            "backend": "redis",
            "type": "white",
            "redis_uri": FakeRedis(decode_responses=True),
            "in_list_life_time": 6000,
        },
    )


@pytest.fixture
def jwt_module_hs_json_black_list():
    return JWTModule(
        alg="HS256",
        secret_key="SECRET",
        list={"backend": "json", "type": "black", "json_path": ":memory:"},
    )


@pytest.fixture
def jwt_module_rs_json_black_list():
    from jam.utils import generate_rsa_key_pair

    keys = generate_rsa_key_pair()

    return JWTModule(
        alg="RS256",
        public_key=keys["public"],
        private_key=keys["private"],
        list={"backend": "json", "type": "black", "json_path": ":memory:"},
    )


@pytest.fixture
def jwt_module_hs_json_white_list():
    return JWTModule(
        alg="HS256",
        secret_key="SECRET",
        list={"backend": "json", "type": "white", "json_path": ":memory:"},
    )


@pytest.fixture
def jwt_module_rs_json_white_list():
    from jam.utils import generate_rsa_key_pair

    keys = generate_rsa_key_pair()

    return JWTModule(
        alg="RS256",
        public_key=keys["public"],
        private_key=keys["private"],
        list={"backend": "json", "type": "white", "json_path": ":memory:"},
    )


def test_payload_maker(jwt_module_hs, jwt_module_rs):
    payload = jwt_module_hs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )

    assert payload["jti"] is not None
    assert payload["user_id"] == 1
    assert payload["username"] == "test_user"

    payload = jwt_module_rs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )

    assert payload["jti"] is not None
    assert payload["user_id"] == 1
    assert payload["username"] == "test_user"


def test_jwt_token_generation(jwt_module_hs, jwt_module_rs):

    from jam.jwt.tools import __validate_jwt__

    payload = jwt_module_hs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )
    token = jwt_module_hs.gen_token(payload=payload)
    assert token is not None
    assert isinstance(token, str)

    decoded_payload = __validate_jwt__(
        token=token,
        secret=jwt_module_hs._secret_key,
        check_exp=False,
        public_key=None,
    )

    assert decoded_payload["payload"] == payload

    payload = jwt_module_rs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )
    token = jwt_module_rs.gen_token(payload=payload)
    assert token is not None
    assert isinstance(token, str)

    decoded_payload = __validate_jwt__(
        token=token,
        secret=None,
        check_exp=False,
        public_key=jwt_module_rs.public_key,
    )

    assert decoded_payload["payload"] == payload


def test_jwt_token_validation(jwt_module_hs, jwt_module_rs):
    payload = jwt_module_hs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )
    token = jwt_module_hs.gen_token(payload=payload)
    assert token is not None
    assert isinstance(token, str)

    decoded_payload = jwt_module_hs.validate_payload(
        token=token, check_exp=False, check_list=False
    )["payload"]
    assert decoded_payload == payload

    with pytest.raises(ValueError):
        jwt_module_hs.validate_payload(
            token=token + "corrupted", check_exp=False, check_list=False
        )

    payload = jwt_module_rs.make_payload(
        exp=3600, **{"user_id": 1, "username": "test_user"}
    )
    token = jwt_module_rs.gen_token(payload=payload)
    assert token is not None
    assert isinstance(token, str)

    decoded_payload = jwt_module_rs.validate_payload(
        token=token, check_exp=False, check_list=False
    )["payload"]
    assert decoded_payload == payload

    with pytest.raises(ValueError):
        jwt_module_rs.validate_payload(
            token=token + "corrupted", check_exp=False, check_list=False
        )


def test_jwt_redis_black_lists(
    jwt_module_hs_redis_black_list, jwt_module_rs_redis_black_list
):

    from jam.exceptions import TokenInBlackList

    # hs
    payload_dict = {"user": 1}

    payload = jwt_module_hs_redis_black_list.make_payload(**payload_dict)
    token = jwt_module_hs_redis_black_list.gen_token(payload=payload)

    # no raises
    token_payload = jwt_module_hs_redis_black_list.validate_payload(
        token=token, check_list=True, check_exp=False
    )

    assert token_payload["payload"]["user"] == payload["user"]

    ## add token to black list
    jwt_module_hs_redis_black_list.list.add(token)

    with pytest.raises(TokenInBlackList):
        jwt_module_hs_redis_black_list.validate_payload(token, check_list=True)

    # rs
    payload = jwt_module_rs_redis_black_list.make_payload(**payload_dict)
    token = jwt_module_rs_redis_black_list.gen_token(payload=payload)

    token_payload = jwt_module_rs_redis_black_list.validate_payload(
        token, check_list=True, check_exp=False
    )

    assert token_payload["payload"]["user"] == payload["user"]

    jwt_module_rs_redis_black_list.list.add(token)

    with pytest.raises(TokenInBlackList):
        jwt_module_rs_redis_black_list.validate_payload(
            token, check_list=True, check_exp=False
        )


def test_jwt_json_black_lists(
    jwt_module_hs_json_black_list, jwt_module_rs_json_black_list
):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    from jam.exceptions import TokenInBlackList

    payload_dict = {"user": 1}

    payload = jwt_module_hs_json_black_list.make_payload(**payload_dict)
    token = jwt_module_hs_json_black_list.gen_token(payload=payload)

    decoded_payload = jwt_module_hs_json_black_list.validate_payload(
        token=token, check_list=True, check_exp=False
    )

    assert decoded_payload["payload"]["user"] == payload_dict["user"]

    jwt_module_hs_json_black_list.list.add(token)

    with pytest.raises(TokenInBlackList):
        jwt_module_hs_json_black_list.validate_payload(
            token, check_list=True, check_exp=False
        )

    t.truncate()

    payload = jwt_module_rs_json_black_list.make_payload(**payload_dict)
    token = jwt_module_rs_json_black_list.gen_token(payload=payload)

    decoded_payload = jwt_module_rs_json_black_list.validate_payload(
        token=token, check_list=True, check_exp=False
    )

    assert decoded_payload["payload"]["user"] == payload_dict["user"]

    jwt_module_rs_json_black_list.list.add(token)

    with pytest.raises(TokenInBlackList):
        jwt_module_rs_json_black_list.validate_payload(
            token, check_list=True, check_exp=False
        )

    t.truncate()


def test_jwt_redis_white_lists(
    jwt_module_hs_redis_white_list, jwt_module_rs_redis_white_list
):
    from jam.exceptions import TokenNotInWhiteList

    payload_dict = {"user": 1}

    payload = jwt_module_hs_redis_white_list.make_payload(**payload_dict)
    token = jwt_module_hs_redis_white_list.gen_token(payload=payload)

    decoded_payload = jwt_module_hs_redis_white_list.validate_payload(
        token, check_list=True, check_exp=False
    )

    assert decoded_payload["payload"]["user"] == payload_dict["user"]

    jwt_module_hs_redis_white_list.list.delete(token)

    with pytest.raises(TokenNotInWhiteList):
        jwt_module_hs_redis_white_list.validate_payload(
            token, check_list=True, check_exp=False
        )

    payload = jwt_module_rs_redis_white_list.make_payload(**payload_dict)
    token = jwt_module_rs_redis_white_list.gen_token(payload=payload)

    decoded_payload = jwt_module_rs_redis_white_list.validate_payload(
        token, check_list=True, check_exp=False
    )

    assert decoded_payload["payload"]["user"] == payload_dict["user"]

    jwt_module_rs_redis_white_list.list.delete(token)

    with pytest.raises(TokenNotInWhiteList):
        jwt_module_rs_redis_white_list.validate_payload(
            token, check_list=True, check_exp=False
        )


def test_jwt_json_white_lists(
    jwt_module_hs_json_white_list, jwt_module_rs_json_white_list
):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    from jam.exceptions import TokenNotInWhiteList

    payload_dict = {"user": 1}

    payload = jwt_module_hs_json_white_list.make_payload(**payload_dict)
    token = jwt_module_hs_json_white_list.gen_token(payload=payload)

    decoded_payload = jwt_module_hs_json_white_list.validate_payload(
        token=token, check_list=True, check_exp=False
    )

    assert decoded_payload["payload"]["user"] == payload_dict["user"]

    jwt_module_hs_json_white_list.list.delete(token)

    with pytest.raises(TokenNotInWhiteList):
        jwt_module_hs_json_white_list.validate_payload(
            token, check_list=True, check_exp=False
        )

    t.truncate()

    payload = jwt_module_rs_json_white_list.make_payload(**payload_dict)
    token = jwt_module_rs_json_white_list.gen_token(payload=payload)

    decoded_payload = jwt_module_rs_json_white_list.validate_payload(
        token=token, check_list=True, check_exp=False
    )

    assert decoded_payload["payload"]["user"] == payload_dict["user"]

    jwt_module_rs_json_white_list.list.delete(token)

    with pytest.raises(TokenNotInWhiteList):
        jwt_module_rs_json_white_list.validate_payload(
            token, check_list=True, check_exp=False
        )

    t.truncate()
