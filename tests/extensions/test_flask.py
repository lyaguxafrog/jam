# -*- coding: utf-8 -*-

import os
import pytest
from flask import Flask, g

from jam.ext.flask import (
    JWTExtension,
    PASETOExtension,
    SessionExtension,
    SimpleUser,
)
from jam.jwt import JWT
from jam.paseto import create_instance as create_paseto
from jam.sessions import create_instance as create_session


@pytest.fixture
def jwt():
    return JWT(alg="HS256", secret="test_secret")


@pytest.fixture
def token(jwt) -> str:
    return jwt.encode({"user_id": 123})


@pytest.fixture
def session():
    path = "test_flask_sessions.json"
    if os.path.exists(path):
        os.remove(path)
    yield create_session(session_type="json", json_path=path)
    if os.path.exists(path):
        os.remove(path)


def test_jwt_get_user_from_header(token, jwt):
    app = Flask(__name__)
    jwt_ext = JWTExtension(
        app, auth=jwt, header_name="Authorization", user=SimpleUser
    )

    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        from flask import request

        user, token_model = jwt_ext.load_user(request)
        assert user is not None
        assert user.payload == {"user_id": 123}
        assert token_model.token == token


def test_jwt_get_user_from_cookie(token, jwt):
    app = Flask(__name__)
    jwt_ext = JWTExtension(
        app, auth=jwt, cookie_name="access_token", user=SimpleUser
    )

    @app.route("/")
    def index():
        from flask import request

        user, _ = jwt_ext.load_user(request)
        return {"user": user.payload if user else None}

    with app.test_client() as client:
        client.set_cookie("access_token", token)
        response = client.get("/")
        assert response.get_json()["user"] == {"user_id": 123}


def test_jwt_get_user_invalid_token(jwt):
    app = Flask(__name__)
    jwt_ext = JWTExtension(
        app, auth=jwt, header_name="Authorization", user=SimpleUser
    )

    with app.test_request_context(
        headers={"Authorization": "Bearer wrong_token"}
    ):
        from flask import request

        with pytest.raises(Exception):
            jwt_ext.load_user(request)


def test_jwt_get_user_no_token(jwt):
    app = Flask(__name__)
    jwt_ext = JWTExtension(
        app, auth=jwt, header_name="Authorization", user=SimpleUser
    )

    with app.test_request_context():
        from flask import request

        user, token_model = jwt_ext.load_user(request)
        assert user is None
        assert token_model.token is None


def test_sessions_get_user_from_header(session):
    app = Flask(__name__)
    session_ext = SessionExtension(
        app, auth=session, header_name="Authorization", user=SimpleUser
    )
    session_id = session.create("test", {"user_id": 123})

    with app.test_request_context(
        headers={"Authorization": f"Bearer {session_id}"}
    ):
        from flask import request

        user, token_model = session_ext.load_user(request)
        assert user is not None
        assert user.payload == {"user_id": 123}


def test_sessions_get_user_from_cookie(session):
    app = Flask(__name__)
    session_ext = SessionExtension(
        app, auth=session, cookie_name="sessionId", user=SimpleUser
    )
    session_id = session.create("test", {"user_id": 123})

    @app.route("/")
    def index():
        from flask import request

        user, _ = session_ext.load_user(request)
        return {"user": user.payload if user else None}

    with app.test_client() as client:
        client.set_cookie("sessionId", session_id)
        response = client.get("/")
        assert response.get_json()["user"] == {"user_id": 123}


def test_sessions_get_user_invalid_token(session):
    app = Flask(__name__)
    session_ext = SessionExtension(
        app, auth=session, header_name="Authorization", user=SimpleUser
    )

    with app.test_request_context(
        headers={"Authorization": "Bearer wrong_session"}
    ):
        from flask import request

        user, token_model = session_ext.load_user(request)
        assert user is None


def test_sessions_get_user_no_token(session):
    app = Flask(__name__)
    session_ext = SessionExtension(
        app, auth=session, header_name="Authorization", user=SimpleUser
    )

    with app.test_request_context():
        from flask import request

        user, token_model = session_ext.load_user(request)
        assert user is None
        assert token_model.token is None


def test_paseto_get_user_from_header():
    import base64

    key = base64.urlsafe_b64encode(b"12345678901234567890123456789012").decode()
    paseto = create_paseto(version="v4", purpose="local", key=key)
    token = paseto.encode({"user_id": 123})

    app = Flask(__name__)
    paseto_ext = PASETOExtension(
        app, auth=paseto, header_name="Authorization", user=SimpleUser
    )

    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        from flask import request

        user, token_model = paseto_ext.load_user(request)
        assert user is not None
        assert user.payload["user_id"] == 123


def test_paseto_get_user_no_token():
    import base64

    key = base64.urlsafe_b64encode(b"12345678901234567890123456789012").decode()
    paseto = create_paseto(version="v4", purpose="local", key=key)

    app = Flask(__name__)
    paseto_ext = PASETOExtension(
        app, auth=paseto, header_name="Authorization", user=SimpleUser
    )

    with app.test_request_context():
        from flask import request

        user, token_model = paseto_ext.load_user(request)
        assert user is None
