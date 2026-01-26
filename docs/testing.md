# Jam testing

For convenient testing of your services that use Jam, you can easily
replace the main Jam instance with a test instance that has the same interface but 
works according to its own rules (for example, always succeeds).

`TestJam` and `TestAsyncJam` provide fake implementations of all Jam methods for testing purposes.
All operations always succeed and return fake but valid data.

!!! tip
    For async services, you can use [`TestAsyncJam`](/api/tests/clients/#jam.tests.clients.TestAsyncJam) instead of `TestJam`.
    The methods are the same, but you need to use `await` keyword.

## Basic usage

For example, you have a service for generating JWT tokens.

```python

from jam import Jam

class AuthService:
    def __init__(
            self,
            jam_instance: Jam
    ) -> None:
        self.jam = jam_instance

    # Generate new token
    def generate_token(self, user: User) -> str:
        payload = self.jam.jwt_make_payload(exp=None, data=user.to_payload())
        token = self.jam.jwt_create_token(payload)
        return token

    # Validate token and return user or None
    def validate_token(self, token) -> User | None:
        try:
            payload = self.jam.jwt_verify_token(
                token, check_exp=True, check_list=False
            )
        except ValueError:
            return None
```

And you need to write tests for it.
```python
import pytest
from jam.tests import TestJam

from your_app.services import AuthService


@pytest.fixture
def auth_service() -> AuthService:
    return AuthService(
        jam_instance=TestJam()  # Use TestJam instance here
    )

def test_auth_user(auth_service):
    user = User(id=1, username="test_user")
    token = auth_service.generate_token(user)  # Generate token
    assert token is not None

    validated_user = auth_service.validate_token(token)  # Validate token
    assert validated_user is not None
    assert validated_user.id == user.id
    assert validated_user.username == user.username

    # if you want to test invalid token
    from jam.tests.fakers import invalid_token
    invalid_user = auth_service.validate_token(invalid_token())
    assert invalid_user is None
```

## JWT testing

```python
import pytest
from jam.tests import TestJam

@pytest.fixture
def client() -> TestJam:
    return TestJam()

def test_jwt_token(client):
    payload = {"user_id": 1, "role": "admin"}
    token = client.jwt_create_token(payload)
    assert isinstance(token, str)
    assert token.count(".") == 2  # JWT tokens have two dots

    verified_payload = client.jwt_verify_token(token, check_exp=False, check_list=False)
    assert verified_payload == payload

def test_invalid_jwt_token(client):
    from jam.tests.fakers import invalid_token
    token = invalid_token()
    with pytest.raises(ValueError):
        client.jwt_verify_token(token, check_exp=False, check_list=False)
```

## Sessions testing

```python
import pytest
from jam.tests import TestJam

@pytest.fixture
def client() -> TestJam:
    return TestJam()

def test_sessions(client):
    # Create session
    session_id = client.session_create(
        session_key="user_session",
        data={"user_id": 1, "username": "test_user"}
    )
    assert session_id is not None

    # Get session data
    session_data = client.session_get(session_id)
    assert session_data == {"user_id": 1, "username": "test_user"}

    # Update session
    client.session_update(session_id, {"role": "admin"})
    updated_data = client.session_get(session_id)
    assert updated_data["role"] == "admin"

    # Delete session
    client.session_delete(session_id)
    assert client.session_get(session_id) is None

    # Clear all sessions by key
    session_id1 = client.session_create("key1", {"data": 1})
    session_id2 = client.session_create("key1", {"data": 2})
    client.session_clear("key1")
    assert client.session_get(session_id1) is None
    assert client.session_get(session_id2) is None
```

## OTP testing

```python
import pytest
from jam.tests import TestJam

@pytest.fixture
def client() -> TestJam:
    return TestJam()

def test_otp(client):
    secret = "test_secret"
    
    # Generate OTP code
    code = client.otp_code(secret)
    assert code == "123456"  # TestJam always returns "123456"

    # Verify OTP code
    assert client.otp_verify_code(secret, "123456") is True
    assert client.otp_verify_code(secret, "wrong_code") is False

    # Generate OTP URI
    uri = client.otp_uri(secret, name="user@example.com", issuer="MyApp")
    assert uri.startswith("otpauth://totp/")
    assert "secret=test_secret" in uri
```

## OAuth2 testing

```python
import pytest
from jam.tests import TestJam

@pytest.fixture
def client() -> TestJam:
    return TestJam()

def test_oauth2(client):
    # Get authorization URL
    url = client.oauth2_get_authorized_url(
        provider="github",
        scope=["read:user"]
    )
    assert "github" in url

    # Fetch token
    tokens = client.oauth2_fetch_token(
        provider="github",
        code="test_code"
    )
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    # Refresh token
    new_tokens = client.oauth2_refresh_token(
        provider="github",
        refresh_token=tokens["refresh_token"]
    )
    assert "access_token" in new_tokens

    # Client credentials flow
    m2m_tokens = client.oauth2_client_credentials_flow(
        provider="github",
        scope=["read:user"]
    )
    assert "access_token" in m2m_tokens
```

## PASETO testing

```python
import pytest
from jam.tests import TestJam

@pytest.fixture
def client() -> TestJam:
    return TestJam()

def test_paseto(client):
    # Make payload
    payload = client.paseto_make_payload(exp=3600, user_id=1, role="admin")
    assert "user_id" in payload
    assert "role" in payload

    # Create PASETO token
    token = client.paseto_create(
        payload=payload,
        footer={"kid": "key1"}
    )
    assert isinstance(token, str)

    # Decode PASETO token
    result = client.paseto_decode(token)
    assert result["payload"]["user_id"] == 1
    assert result["footer"]["kid"] == "key1"
```

## Async testing

For async services, use `TestAsyncJam`:

```python
import pytest
import pytest_asyncio
from jam.tests import TestAsyncJam

@pytest_asyncio.fixture
async def client() -> TestAsyncJam:
    return TestAsyncJam()

@pytest.mark.asyncio
async def test_async_jwt(client):
    payload = {"user_id": 1, "role": "admin"}
    token = await client.jwt_create_token(payload)
    assert isinstance(token, str)

    verified_payload = await client.jwt_verify_token(token, check_exp=False, check_list=False)
    assert verified_payload == payload

@pytest.mark.asyncio
async def test_async_sessions(client):
    session_id = await client.session_create(
        session_key="user_session",
        data={"user_id": 1}
    )
    session_data = await client.session_get(session_id)
    assert session_data == {"user_id": 1}
```