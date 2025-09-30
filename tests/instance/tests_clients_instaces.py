# -*- coding: utf-8 -*-

import pytest
from pytest_asyncio import fixture

from jam.tests import TestAsyncJam, TestJam
from jam.tests.fakers import invalid_token


@pytest.fixture
def client_instance() -> TestJam:
    return TestJam()


@fixture
async def async_client_instance() -> TestAsyncJam:
    return TestAsyncJam()


def test_client_instance(client_instance):
    payload = client_instance.make_payload(**{"user": 1})
    valid_token = client_instance.gen_jwt_token(payload)

    verify = client_instance.verify_jwt_token(valid_token)
    assert verify == payload

    invalid_token_ = invalid_token()

    with pytest.raises(ValueError):
        client_instance.verify_jwt_token(invalid_token_)

    session_id = client_instance.create_session(
        session_key="TEST", data={"user": 1}
    )

    session_data = client_instance.get_session(session_id)
    assert session_data == {"user": 1}

    otp_code = client_instance.get_otp_code(
        secret="fdfdfd",
    )

    assert (
        client_instance.verify_otp_code(
            secret="fdfd", code=otp_code, factor=None, look_ahead=1
        )
        is True
    )

    assert (
        client_instance.verify_otp_code(
            secret="fdfd", code="dfdfd", factor=None, look_ahead=1
        )
        is False
    )


@pytest.mark.asyncio
async def test_client_instance(async_client_instance):
    payload = await async_client_instance.make_payload(**{"user": 1})
    valid_token = await async_client_instance.gen_jwt_token(payload)

    verify = await async_client_instance.verify_jwt_token(valid_token)
    assert verify == payload

    invalid_token_ = invalid_token()

    with pytest.raises(ValueError):
        await async_client_instance.verify_jwt_token(invalid_token_)

    session_id = await async_client_instance.create_session(
        session_key="TEST", data={"user": 1}
    )

    session_data = await async_client_instance.get_session(session_id)
    assert session_data == {"user": 1}

    otp_code = await async_client_instance.get_otp_code(
        secret="fdfdfd",
    )

    assert (
        await async_client_instance.verify_otp_code(
            secret="fdfd", code=otp_code, factor=None, look_ahead=1
        )
        is True
    )

    assert (
        await async_client_instance.verify_otp_code(
            secret="fdfd", code="dfdfd", factor=None, look_ahead=1
        )
        is False
    )
