# Jam testing

For convenient testing of your services that use Jam, you can easily
replace the main Jam instance with a test instance that has the same interface but 
works according to its own rules (for example, always succeeds).

For example, you have a service for generating JWT tokens.

!!! tip
    For async services, you can use [`TestAsyncJam`](/api/tests/clients/#jam.tests.clients.TestAsyncJam) instead of `TestJam`.

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