# -*- coding: utf-8 -*-

import pytest
from flask import Flask

from jam.ext.flask import JWTExtension, SessionExtension
from jam.tests import TestJam
from jam.tests.fakers import fake_jwt_token


@pytest.fixture
def token() -> str:
    return fake_jwt_token({"user_id": 123})


def test_jwt_get_payload_from_header(token):
    app = Flask(__name__)
    jam = TestJam()
    jwt_ext = JWTExtension(jam, app, header_name="Authorization")

    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        payload = jwt_ext._get_payload()
        assert payload == {"user_id": 123}


def test_jwt_get_payload_from_cookie(token):
    app = Flask(__name__)
    jam = TestJam()
    jwt_ext = JWTExtension(jam, app, cookie_name="access_token")
    jwt_ext.init_app(app)

    with app.test_client() as client:
        client.set_cookie("access_token", token)
        response = client.get("/")
        from flask import g

        assert g.payload == {"user_id": 123}


def test_jwt_get_payload_invalid_token():
    app = Flask(__name__)
    jam = TestJam()
    jwt_ext = JWTExtension(jam, app, header_name="Authorization")

    with app.test_request_context(
        headers={"Authorization": "Bearer wrong_token"}
    ):
        payload = jwt_ext._get_payload()
        assert payload is None


def test_sessions_get_payload_from_header():
    app = Flask(__name__)
    jam = TestJam()
    jwt_ext = SessionExtension(jam, app, header_name="Authorization")
    session_id = jam.create_session("test", {"user_id": 123})

    with app.test_request_context(
        headers={"Authorization": f"Bearer {session_id}"}
    ):
        payload = jwt_ext._get_payload()
        assert payload == {"user_id": 123}


def test_sessions_get_payload_from_cookie():
    app = Flask(__name__)
    jam = TestJam()
    jwt_ext = SessionExtension(jam, app, cookie_name="sessionId")
    jwt_ext.init_app(app)
    session_id = jam.create_session("test", {"user_id": 123})

    with app.test_client() as client:
        client.set_cookie("sessionId", session_id)
        response = client.get("/")
        from flask import g

        assert g.payload == {"user_id": 123}


def test_sessions_get_payload_invalid_token():
    app = Flask(__name__)
    jam = TestJam()
    jwt_ext = SessionExtension(jam, app, header_name="Authorization")

    with app.test_request_context(
        headers={"Authorization": "Bearer wrong_session"}
    ):
        payload = jwt_ext._get_payload()
        assert payload is None
