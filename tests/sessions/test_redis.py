# -*- coding: utf-8 -*-

from threading import Thread

import pytest
from fakeredis import TcpFakeServer
from pytest import fixture
from redis import Redis

from jam.sessions.redis import RedisSessions


@fixture(scope="session", autouse=True)
def fake_redis():
    server = TcpFakeServer(("0.0.0.0", 6379), server_type="redis")
    t = Thread(target=server.serve_forever, daemon=True)
    t.start()


@fixture(scope="function")
def redis_session_instance_no_crypt(fake_redis):
    return RedisSessions(
        redis_uri="redis://0.0.0.0:6379",
        redis_sessions_key="test",
        default_ttl=None,
        is_session_crypt=False,
    )


def test_create_new_session(redis_session_instance_no_crypt):
    session = redis_session_instance_no_crypt.create(
        session_key="test", data={"user_id": 1}
    )

    assert isinstance(session, str)
    assert len(session) > 0
    assert (session.split(":")[0]) == "test"

    redis = Redis.from_url("redis://0.0.0.0:6379", decode_responses=True)
    stored_data = redis.hget(name="test:test", key=session)

    assert stored_data == '{"user_id": 1}'


def test_get_session(redis_session_instance_no_crypt):
    session = redis_session_instance_no_crypt.create(
        session_key="test", data={"user_id": 1}
    )

    retrieved_data = redis_session_instance_no_crypt.get(session)
    assert retrieved_data == {"user_id": 1}


def test_get_nonexistent_session(redis_session_instance_no_crypt):
    retrieved_data = redis_session_instance_no_crypt.get("nonexistent:session")
    assert retrieved_data is None


def test_delete_session(redis_session_instance_no_crypt):
    session = redis_session_instance_no_crypt.create(
        session_key="test", data={"user_id": 1}
    )
    redis_session_instance_no_crypt.delete(session)
    retrieved_data = redis_session_instance_no_crypt.get(session)
    assert retrieved_data is None


def test_session_ttl(redis_session_instance_no_crypt):
    redis_session_instance_no_crypt.ttl = 20  # Set TTL to 2 seconds
    session = redis_session_instance_no_crypt.create(
        session_key="test", data={"user_id": 1}
    )
    redis = Redis.from_url("redis://0.0.0.0:6379", decode_responses=True)
    ttl = redis.httl("test:test", session)[0]
    assert ttl <= 20 and ttl > 0


def test_update_session(redis_session_instance_no_crypt):
    session = redis_session_instance_no_crypt.create(
        session_key="test", data={"user_id": 1}
    )
    redis_session_instance_no_crypt.update(session, {"user_id": 2})
    retrieved_data = redis_session_instance_no_crypt.get(session)
    assert retrieved_data == {"user_id": 2}


def test_update_nonexistent_session(redis_session_instance_no_crypt):
    with pytest.raises(KeyError):
        redis_session_instance_no_crypt.update(
            "nonexistent:session", {"user_id": 2}
        )


def test_create_session_no_data(redis_session_instance_no_crypt):
    session = redis_session_instance_no_crypt.create(session_key="test")
    assert isinstance(session, str)
    assert len(session) > 0
    assert (session.split(":")[0]) == "test"
    retrieved_data = redis_session_instance_no_crypt.get(session)
    assert retrieved_data is None


def test_create_session_empty_data(redis_session_instance_no_crypt):
    session = redis_session_instance_no_crypt.create(
        session_key="test", data={}
    )
    assert isinstance(session, str)
    assert len(session) > 0
    assert (session.split(":")[0]) == "test"
    retrieved_data = redis_session_instance_no_crypt.get(session)
    assert retrieved_data == {}
