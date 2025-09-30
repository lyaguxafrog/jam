# -*- coding: utf-8 -*-

import pytest
from fakeredis import FakeRedis

from jam.modules import SessionModule


@pytest.fixture
def session_redis_no_crypt_module():
    return SessionModule(
        sessions_type="redis",
        is_session_crypt=False,
        sessions_path="test",
        redis_uri=FakeRedis(decode_responses=True),
    )


@pytest.fixture
def session_json_no_crypt_module():
    return SessionModule(
        sessions_type="json", is_session_crypt=False, json_path=":memory:"
    )


@pytest.fixture
def session_redis_crypt_module():
    from jam.utils import generate_aes_key

    key = generate_aes_key()

    return SessionModule(
        sessions_type="redis",
        is_session_crypt=True,
        session_aes_secret=key,
        redis_uri=FakeRedis(decode_responses=True),
        sessions_path="test",
    )


@pytest.fixture
def session_json_crypt_module():
    from jam.utils import generate_aes_key

    key = generate_aes_key()

    return SessionModule(
        sessions_type="json",
        is_session_crypt=True,
        session_aes_secret=key,
        json_path=":memory:",
    )


def test_session_redis_no_crypt_create(session_redis_no_crypt_module):
    session = session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )

    assert isinstance(session, str)
    assert len(session) > 0
    assert (session.split(":")[0]) == "test"

    stored_data = session_redis_no_crypt_module.module._redis.hget(
        name="test:test", key=session
    )

    assert stored_data == '{"user_id": 1}'


def test_session_json_no_crypt_create(session_json_no_crypt_module):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    session = session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )

    assert isinstance(session, str)
    assert len(session) > 0

    stored_data = session_json_no_crypt_module.get(session)

    assert stored_data == {"user_id": 1}
    t.truncate()


def test_session_redis_no_crypt_get(session_redis_no_crypt_module):
    session = session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    data = session_redis_no_crypt_module.get(session)

    assert data == {"user_id": 1}


def test_session_json_no_crypt_get(session_json_no_crypt_module):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    session = session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    data = session_json_no_crypt_module.get(session)
    assert data == {"user_id": 1}
    t.truncate()


def test_session_redis_no_crypt_delete(session_redis_no_crypt_module):
    session = session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    session_redis_no_crypt_module.delete(session)
    data = session_redis_no_crypt_module.get(session)

    assert data is None


def test_session_json_no_crypt_delete(session_json_no_crypt_module):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    session = session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    session_json_no_crypt_module.delete(session)
    data = session_json_no_crypt_module.get(session)
    assert data is None
    t.truncate()


def test_session_redis_no_crypt_update(session_redis_no_crypt_module):
    session = session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    session_redis_no_crypt_module.update(session, {"user_id": 2})
    data = session_redis_no_crypt_module.get(session)

    assert data == {"user_id": 2}


def test_session_json_no_crypt_update(session_json_no_crypt_module):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    session = session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    session_json_no_crypt_module.update(session, {"user_id": 2})
    data = session_json_no_crypt_module.get(session)
    assert data == {"user_id": 2}
    t.truncate()


def test_session_redis_no_crypt_get_nonexistent(session_redis_no_crypt_module):
    data = session_redis_no_crypt_module.get("nonexistent:session")
    assert data is None


def test_session_json_no_crypt_get_nonexistent(session_json_no_crypt_module):
    data = session_json_no_crypt_module.get("nonexistent:session")
    assert data is None


def test_session_redis_no_crypt_clear(session_redis_no_crypt_module):
    session1 = session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    session2 = session_redis_no_crypt_module.create(
        session_key="test", data={"user_id": 2}
    )
    session_redis_no_crypt_module.clear("test")
    data1 = session_redis_no_crypt_module.get(session1)
    data2 = session_redis_no_crypt_module.get(session2)

    assert data1 is None
    assert data2 is None


def test_session_json_no_crypt_clear(session_json_no_crypt_module):
    from tinydb import TinyDB

    t = TinyDB(":memory:")
    t.truncate()

    session1 = session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    session2 = session_json_no_crypt_module.create(
        session_key="test", data={"user_id": 2}
    )
    session_json_no_crypt_module.clear("test")
    data1 = session_json_no_crypt_module.get(session1)
    data2 = session_json_no_crypt_module.get(session2)

    assert data1 is None
    assert data2 is None
    t.truncate()


def test_session_crypts(session_redis_crypt_module, session_json_crypt_module):
    session = session_redis_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )

    assert isinstance(session, str)
    assert len(session) > 0
    assert session.startswith("test:") is False
    assert session.startswith("J$_")

    data = session_redis_crypt_module.get(session)
    assert data == {"user_id": 1}

    session_redis_crypt_module.update(session, {"user_id": 2})
    data = session_redis_crypt_module.get(session)
    assert data == {"user_id": 2}

    session_redis_crypt_module.delete(session)
    data = session_redis_crypt_module.get(session)
    assert data is None

    session = session_json_crypt_module.create(
        session_key="test", data={"user_id": 1}
    )
    assert isinstance(session, str)
    assert len(session) > 0
    assert session.startswith("test:") is False
    assert session.startswith("J$_")
    data = session_json_crypt_module.get(session)
    assert data == {"user_id": 1}

    session_json_crypt_module.update(session, {"user_id": 2})
    data = session_json_crypt_module.get(session)
    assert data == {"user_id": 2}

    session_json_crypt_module.delete(session)
    data = session_json_crypt_module.get(session)
    assert data is None
