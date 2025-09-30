# -*- coding: utf-8 -*-

import pytest
from fakeredis import FakeAsyncRedis
from pytest_asyncio import fixture

from jam.aio.modules import SessionModule


@fixture
async def session_redis_no_crypt_module():
    return SessionModule(
        sessions_type="redis",
        is_session_crypt=False,
        sessions_path="test",
        redis_uri=FakeAsyncRedis(decode_responses=True),
    )


@fixture
async def session_json_no_crypt_module():
    return SessionModule(
        sessions_type="json", is_session_crypt=False, json_path=":memory:"
    )


@fixture
async def session_redis_crypt_module():
    from jam.utils import generate_aes_key

    key = generate_aes_key()

    return SessionModule(
        sessions_type="redis",
        is_session_crypt=True,
        session_aes_secret=key,
        redis_uri=FakeAsyncRedis(decode_responses=True),
        sessions_path="test",
    )


@fixture
async def session_json_crypt_module():
    from jam.utils import generate_aes_key

    key = generate_aes_key()

    return SessionModule(
        sessions_type="json",
        is_session_crypt=True,
        session_aes_secret=key,
        json_path=":memory:",
    )


@pytest.mark.asyncio
async def test_session_redis_no_crypt_create(session_redis_no_crypt_module):
    session = await session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )

    assert isinstance(session, str)
    assert len(session) > 0
    assert (session.split(":")[0]) == "test"

    stored_data = await session_redis_no_crypt_module.module._redis.hget(
        name="test:test", key=session
    )

    assert stored_data == '{"user_id": 1}'


@pytest.mark.asyncio
async def test_session_json_no_crypt_create(session_json_no_crypt_module):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    session = await session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )

    assert isinstance(session, str)
    assert len(session) > 0

    stored_data = await session_json_no_crypt_module.get(session)

    assert stored_data == {"user_id": 1}
    t.truncate()


@pytest.mark.asyncio
async def test_session_redis_no_crypt_get(session_redis_no_crypt_module):
    session = await session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    data = await session_redis_no_crypt_module.get(session)

    assert data == {"user_id": 1}


@pytest.mark.asyncio
async def test_session_json_no_crypt_get(session_json_no_crypt_module):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    session = await session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    data = await session_json_no_crypt_module.get(session)
    assert data == {"user_id": 1}
    t.truncate()


@pytest.mark.asyncio
async def test_session_redis_no_crypt_delete(session_redis_no_crypt_module):
    session = await session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    await session_redis_no_crypt_module.delete(session)
    data = await session_redis_no_crypt_module.get(session)

    assert data is None


@pytest.mark.asyncio
async def test_session_json_no_crypt_delete(session_json_no_crypt_module):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    session = await session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    await session_json_no_crypt_module.delete(session)
    data = await session_json_no_crypt_module.get(session)
    assert data is None
    t.truncate()


@pytest.mark.asyncio
async def test_session_redis_no_crypt_update(session_redis_no_crypt_module):
    session = await session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    await session_redis_no_crypt_module.update(session, {"user_id": 2})
    data = await session_redis_no_crypt_module.get(session)

    assert data == {"user_id": 2}


@pytest.mark.asyncio
async def test_session_json_no_crypt_update(session_json_no_crypt_module):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    session = await session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    await session_json_no_crypt_module.update(session, {"user_id": 2})
    data = await session_json_no_crypt_module.get(session)
    assert data == {"user_id": 2}
    t.truncate()


@pytest.mark.asyncio
async def test_session_redis_no_crypt_get_nonexistent(
    session_redis_no_crypt_module,
):
    data = await session_redis_no_crypt_module.get("nonexistent:session")
    assert data is None


@pytest.mark.asyncio
async def test_session_json_no_crypt_get_nonexistent(
    session_json_no_crypt_module,
):
    data = await session_json_no_crypt_module.get("nonexistent:session")
    assert data is None


@pytest.mark.asyncio
async def test_session_redis_no_crypt_clear(session_redis_no_crypt_module):
    session1 = await session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    session2 = await session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 2}
    )
    await session_redis_no_crypt_module.clear("test")
    data1 = await session_redis_no_crypt_module.get(session1)
    data2 = await session_redis_no_crypt_module.get(session2)

    assert data1 is None
    assert data2 is None


@pytest.mark.asyncio
async def test_session_json_no_crypt_clear(session_json_no_crypt_module):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    session1 = await session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    session2 = await session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 2}
    )
    await session_json_no_crypt_module.clear("test")
    data1 = await session_json_no_crypt_module.get(session1)
    data2 = await session_json_no_crypt_module.get(session2)

    assert data1 is None
    assert data2 is None
    t.truncate()


@pytest.mark.asyncio
async def test_session_crypts(
    session_redis_crypt_module, session_json_crypt_module
):
    session = await session_redis_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )

    assert isinstance(session, str)
    assert len(session) > 0
    assert session.startswith("test:") is False
    assert session.startswith("J$_")

    data = await session_redis_crypt_module.get(session)
    assert data == {"user_id": 1}

    await session_redis_crypt_module.update(session, {"user_id": 2})
    data = await session_redis_crypt_module.get(session)
    assert data == {"user_id": 2}

    await session_redis_crypt_module.delete(session)
    data = await session_redis_crypt_module.get(session)
    assert data is None

    session = await session_json_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    assert isinstance(session, str)
    assert len(session) > 0
    assert session.startswith("test:") is False
    assert session.startswith("J$_")
    data = await session_json_crypt_module.get(session)
    assert data == {"user_id": 1}

    await session_json_crypt_module.update(session, {"user_id": 2})
    data = await session_json_crypt_module.get(session)
    assert data == {"user_id": 2}

    await session_json_crypt_module.delete(session)
    data = await session_json_crypt_module.get(session)
    assert data is None
