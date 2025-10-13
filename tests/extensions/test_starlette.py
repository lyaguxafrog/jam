# -*- coding: utf-8 -*-

import pytest
from pytest_asyncio import fixture
from starlette.authentication import AuthenticationError
from starlette.requests import HTTPConnection

from jam.ext.starlette.auth_backends import JWTBackend, SessionBackend
from jam.tests import TestAsyncJam, TestJam


@pytest.fixture
def jam() -> TestJam:
    return TestJam()


@fixture
async def async_jam() -> TestAsyncJam:
    return TestAsyncJam()


@pytest.mark.asyncio
async def test_jwt_backend_from_cookie(async_jam):
    backend = JWTBackend(async_jam, cookie_name="access_token")

    conn = HTTPConnection(
        {"type": "http", "headers": [(b"cookie", b"access_token=valid_token")]}
    )

    async_jam.verify_jwt_token = async_jam._async_mock(
        return_value={"user_id": 1, "username": "bob"}
    )

    result = await backend.authenticate(conn)

    assert result is not None
    creds, user = result
    assert creds.scopes == ["authenticated"]
    assert user.payload["user_id"] == 1


@pytest.mark.asyncio
async def test_jwt_backend_from_header(async_jam):
    backend = JWTBackend(async_jam)
    conn = HTTPConnection(
        {"type": "http", "headers": [(b"authorization", b"Bearer valid_token")]}
    )

    async_jam.verify_jwt_token = async_jam._async_mock(
        return_value={"user": "header_user"}
    )

    creds, user = await backend.authenticate(conn)
    assert user.payload == {"user": "header_user"}


@pytest.mark.asyncio
async def test_jwt_backend_no_token_returns_none(async_jam):
    backend = JWTBackend(async_jam)
    conn = HTTPConnection({"type": "http", "headers": []})

    result = await backend.authenticate(conn)
    assert result is None


@pytest.mark.asyncio
async def test_jwt_backend_invalid_token(async_jam):
    backend = JWTBackend(async_jam)
    conn = HTTPConnection(
        {"type": "http", "headers": [(b"authorization", b"Bearer bad")]}
    )

    async def raise_error(*args, **kwargs):
        raise ValueError("Invalid token")

    async_jam.verify_jwt_token = raise_error

    with pytest.raises(AuthenticationError):
        await backend.authenticate(conn)


@pytest.mark.asyncio
async def test_session_backend_from_cookie(async_jam):
    backend = SessionBackend(async_jam, cookie_name="sessionId")

    conn = HTTPConnection(
        {"type": "http", "headers": [(b"cookie", b"sessionId=sid123")]}
    )

    async_jam.get_session = async_jam._async_mock(
        return_value={"user_id": 42, "role": "admin"}
    )

    result = await backend.authenticate(conn)

    assert result is not None
    creds, user = result
    assert creds.scopes == ["authenticated"]
    assert user.payload["user_id"] == 42


@pytest.mark.asyncio
async def test_session_backend_from_header(async_jam):
    backend = SessionBackend(
        async_jam, cookie_name=None, header_name="Authorization"
    )
    conn = HTTPConnection(
        {"type": "http", "headers": [(b"authorization", b"Bearer session123")]}
    )

    async_jam.get_session = async_jam._async_mock(
        return_value={"user": "header_user"}
    )

    creds, user = await backend.authenticate(conn)
    assert user.payload == {"user": "header_user"}


@pytest.mark.asyncio
async def test_session_backend_no_session(async_jam):
    backend = SessionBackend(async_jam)
    conn = HTTPConnection({"type": "http", "headers": []})
    result = await backend.authenticate(conn)
    assert result is None


@pytest.mark.asyncio
async def test_session_backend_invalid_session(async_jam):
    backend = SessionBackend(async_jam, header_name="Authorization")

    conn = HTTPConnection(
        {
            "type": "http",
            "headers": [(b"authorization", b"Bearer broken")],
        }
    )

    async_jam.get_session = async_jam._async_mock(return_value=None)

    result = await backend.authenticate(conn)

    assert result is not None
    creds, user = result
    assert creds.scopes == ["authenticated"]
    assert user.payload is None
