# -*- coding: utf-8 -*-

import pytest
from fakeredis import FakeRedis

from jam import Jam


@pytest.fixture
def jam_jwt_instance():
    jam = Jam(config={"jwt": {"alg": "HS256", "secret_key": "SECRET"}})
    return jam


@pytest.fixture
def jam_session_instance():
    jam = Jam(
        config={
            "session": {
                "sessions_type": "redis",
                "redis_uri": FakeRedis(decode_responses=True),
            }
        }
    )
    return jam


def test_jwt_instance(jam_jwt_instance):
    jwt_payload = jam_jwt_instance.make_payload(
        exp=89898989, **{"sub": "user123"}
    )
    assert jwt_payload["sub"] == "user123"

    token = jam_jwt_instance.gen_jwt_token(jwt_payload)
    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # JWT has three parts separated by dots
    decoded_payload = jam_jwt_instance.verify_jwt_token(
        token, check_exp=False, check_list=False
    )
    assert decoded_payload == jwt_payload


def test_session_instance(jam_session_instance):
    session_data = {"user_id": "user123"}
    session_id = jam_session_instance.create_session(
        session_key="user", data=session_data
    )
    assert isinstance(session_id, str)
    assert len(session_id) > 0

    retrieved_data = jam_session_instance.get_session(session_id)
    assert retrieved_data == session_data

    jam_session_instance.delete_session(session_id)
    assert jam_session_instance.get_session(session_id) is None
