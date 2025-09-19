## JWT

```python
import strawberry
from strawberry.types import Info
from jam import Jam
from typing import Optional


config = {
    "auth_type": "jwt",
    "secret_key": "SECRET"
}

jam = Jam(config)


@strawberry.type
class AuthPayload:
    token: str


@strawberry.type
class User:
    username: str


@strawberry.type
class Query:
    @strawberry.field
    def get_user(self, info: Info, token: str) -> User:
        payload = jam.verify_jwt_token(token, False, False)
        return User(username=payload["username"])


@strawberry.type
class Mutation:
    @strawberry.mutation
    def auth_user(self, username: str, password: str) -> AuthPayload:
        token = jam.gen_jwt_token({"username": username})
        return AuthPayload(token=token)


schema = strawberry.Schema(query=Query, mutation=Mutation)
```

## Sessions

```python
import strawberry
from strawberry.types import Info
from jam import Jam
from typing import Optional


config = {
    "auth_type": "session",
    "session_type": "redis",
    "is_session_crypt": False,
    "redis_uri": "redis://0.0.0.0:6379/0"
}

jam = Jam(config)


@strawberry.type
class SessionPayload:
    session_id: str


@strawberry.type
class User:
    username: str


@strawberry.type
class Query:
    @strawberry.field
    def get_user(self, info: Info, session_id: str) -> User:
        data = jam.get_session(session_id)
        return User(username=data["username"])


@strawberry.type
class Mutation:
    @strawberry.mutation
    def auth_user(self, username: str, password: str) -> SessionPayload:
        session_id = jam.create_session(
            session_key=username,
            data={
                "username": username,
                "another": "data"
            }
        )
        return SessionPayload(session_id=session_id)


schema = strawberry.Schema(query=Query, mutation=Mutation)
```
