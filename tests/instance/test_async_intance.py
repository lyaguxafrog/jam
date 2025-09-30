# -*- coding: utf-8 -*-

import pytest
from fakeredis import FakeAsyncRedis
from pytest_asyncio import fixture

from jam.aio import Jam


@fixture
async def jam_jwt_instance():
    jam = Jam(
        config={"auth_type": "jwt", "alg": "HS256", "secret_key": "SECRET"}
    )
    return jam


@fixture
async def jam_session_instance():
    jam = Jam(
        config={
            "auth_type": "session",
            "sessions_type": "redis",
            "redis_uri": FakeAsyncRedis(decode_responses=True),
        }
    )
    return jam


@pytest.mark.asyncio
async def test_jwt_instance(jam_jwt_instance):
    jwt_payload = await jam_jwt_instance.make_payload(
        exp=89898989, **{"sub": "user123"}
    )
    assert jwt_payload["sub"] == "user123"

    token = await jam_jwt_instance.gen_jwt_token(jwt_payload)
    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # JWT has three parts separated by dots
    decoded_payload = await jam_jwt_instance.verify_jwt_token(
        token, check_exp=False, check_list=False
    )
    assert decoded_payload == jwt_payload


@pytest.mark.asyncio
async def test_session_instance(jam_session_instance):
    session_data = {"user_id": "user123"}
    session_id = await jam_session_instance.create_session(
        session_key="user", data=session_data
    )
    assert isinstance(session_id, str)
    assert len(session_id) > 0

    retrieved_data = await jam_session_instance.get_session(session_id)
    assert retrieved_data == session_data

    await jam_session_instance.delete_session(session_id)
    assert await jam_session_instance.get_session(session_id) is None
