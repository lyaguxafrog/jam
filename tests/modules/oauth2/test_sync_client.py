import json
from unittest.mock import MagicMock, patch

import pytest

from jam.oauth2.client import OAuth2Client


@pytest.fixture
def client():
    return OAuth2Client(
        client_id="abc123",
        client_secret="secret",
        auth_url="https://example.com/auth",
        token_url="https://example.com/token",
        redirect_url="https://example.com/callback",
    )


def test_get_authorization_url_basic(client):
    url = client.get_authorization_url(["email", "profile"], state="xyz")
    assert url.startswith("https://example.com/auth?")
    assert "scope=email+profile" in url
    assert "client_id=abc123" in url
    assert "redirect_uri=https%3A%2F%2Fexample.com%2Fcallback" in url
    assert "state=xyz" in url


def test_fetch_token_success(client):
    fake_response_data = {"access_token": "xyz", "token_type": "Bearer"}

    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(fake_response_data).encode(
        "utf-8"
    )
    mock_response.status = 200

    with patch("jam.oauth2.client.HTTPSConnection") as MockConn:
        conn = MockConn.return_value
        conn.getresponse.return_value = mock_response

        token = client.fetch_token("auth_code_123")

        assert token == fake_response_data

        conn.request.assert_called_once()

        args, kwargs = conn.request.call_args
        method, path = args
        body = kwargs.get("body", "")
        headers = kwargs.get("headers", {})

        assert method == "POST"
        assert "grant_type=authorization_code" in body
        assert "client_id=abc123" in body
        assert "auth_code_123" in body
        assert headers["Content-Type"] == "application/x-www-form-urlencoded"


def test_fetch_token_http_error(client):
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"error": "invalid_grant"}'
    mock_response.status = 400

    with patch("jam.oauth2.client.HTTPSConnection") as MockConn:
        conn = MockConn.return_value
        conn.getresponse.return_value = mock_response

        with pytest.raises(RuntimeError) as e:
            client.fetch_token("bad_code")

        assert "invalid_grant" in str(e.value)


def test_fetch_token_empty_response(client):
    mock_response = MagicMock()
    mock_response.read.return_value = b""
    mock_response.status = 200

    with patch("jam.oauth2.client.HTTPSConnection") as MockConn:
        conn = MockConn.return_value
        conn.getresponse.return_value = mock_response

        with pytest.raises(ValueError, match="Empty response"):
            client.fetch_token("auth_code")


def test_refresh_token_success(client):
    fake_response_data = {"access_token": "new_token", "token_type": "Bearer"}

    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(fake_response_data).encode(
        "utf-8"
    )
    mock_response.status = 200

    with patch("jam.oauth2.client.HTTPSConnection") as MockConn:
        conn = MockConn.return_value
        conn.getresponse.return_value = mock_response

        token = client.refresh_token("refresh123")
        assert token == fake_response_data

        # Проверяем параметры вызова
        args, kwargs = conn.request.call_args
        method, path = args
        body = kwargs.get("body", "")
        headers = kwargs.get("headers", {})

        assert method == "POST"
        assert "grant_type=refresh_token" in body
        assert "refresh_token=refresh123" in body
        assert "client_id=abc123" in body
        assert headers["Content-Type"] == "application/x-www-form-urlencoded"


def test_client_credentials_flow_success(client):
    fake_response_data = {"access_token": "xyz", "expires_in": 3600}

    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(fake_response_data).encode(
        "utf-8"
    )
    mock_response.status = 200

    with patch("jam.oauth2.client.HTTPSConnection") as MockConn:
        conn = MockConn.return_value
        conn.getresponse.return_value = mock_response

        token = client.client_credentials_flow(["read", "write"])
        assert token == fake_response_data

        args, kwargs = conn.request.call_args
        method, path = args
        body = kwargs.get("body", "")
        headers = kwargs.get("headers", {})

        assert method == "POST"
        assert "grant_type=client_credentials" in body
        assert "scope=read+write" in body
        assert "client_id=abc123" in body
        assert "client_secret=secret" in body
        assert headers["Content-Type"] == "application/x-www-form-urlencoded"


def test_post_form_urlencoded_response(client):
    mock_response = MagicMock()
    mock_response.read.return_value = b"access_token=abc123&token_type=Bearer"
    mock_response.status = 200

    with patch("jam.oauth2.client.HTTPSConnection") as MockConn:
        conn = MockConn.return_value
        conn.getresponse.return_value = mock_response

        result = client._OAuth2Client__post_form(
            "https://example.com/token",
            {"a": "b"},
        )
        assert result == {"access_token": "abc123", "token_type": "Bearer"}
