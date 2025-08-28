# -*- coding: utf-8 -*-

import pytest
from tinydb import Query, TinyDB

from jam.sessions.json import JSONSessions


t = TinyDB(":memory:")
ts = Query()


@pytest.fixture(scope="function")
def json_sessions_no_crypt():
    return JSONSessions(
        json_path=":memory:",
        is_session_crypt=False,
    )


def test_create_session(json_sessions_no_crypt):
    session = json_sessions_no_crypt.create(
        session_key="test", data={"user": "test_user"}
    )

    assert isinstance(session, str)
    assert len(session) > 0
    assert (session.split(":")[0]) == "test"

    stored_data = t.search(ts.session_id == session)
    assert stored_data[0]["data"] == {"user": "test_user"}

    t.truncate()


def test_get_session(json_sessions_no_crypt):
    session = json_sessions_no_crypt.create(
        session_key="test", data={"user": "test_user"}
    )
    retrieved_data = json_sessions_no_crypt.get(session)
    assert retrieved_data == {"user": "test_user"}

    t.truncate()


def test_get_nonexistent_session(json_sessions_no_crypt):
    retrieved_data = json_sessions_no_crypt.get("nonexistent:session")
    assert retrieved_data is None

    t.truncate()


def test_delete_session(json_sessions_no_crypt):
    session = json_sessions_no_crypt.create(
        session_key="test", data={"user": "test_user"}
    )
    json_sessions_no_crypt.delete(session)
    retrieved_data = json_sessions_no_crypt.get(session)
    assert retrieved_data is None

    t.truncate()


def test_update_session(json_sessions_no_crypt):
    session = json_sessions_no_crypt.create(
        session_key="test", data={"user": "test_user"}
    )
    json_sessions_no_crypt.update(session, {"user": "updated_user"})
    retrieved_data = json_sessions_no_crypt.get(session)
    assert retrieved_data == {"user": "updated_user"}

    t.truncate()


def test_update_nonexistent_session(json_sessions_no_crypt):
    json_sessions_no_crypt.update(
        "nonexistent:session", {"user": "updated_user"}
    )
    retrieved_data = json_sessions_no_crypt.get("nonexistent:session")
    assert retrieved_data is None

    t.truncate()
