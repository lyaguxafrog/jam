---
title: Jam + Starlette = <3
---

# Starlette integration

Integration with Starlet is implemented using [authorization backends for middlewares](https://starlette.dev/authentication/).

## How it works

All you need to do is pass the relevant authorization backend to the middleware, and everything will work. Jam implements middleware that checks the `header` or `cookie` (depending on your settings) and packages the data into the `request`.

Example:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from jam.ext.starlette import JWTBackend  # for example


async def get_profile(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    return PlainTextResponse(request.user.username)


app = Starlette(
    routes=[Route("/profile", get_profile, methods=["GET"])],
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=JWTBackend(
                config="config.toml",
                cookie_name="jwt"
            ),
        )
    ]
)
```

## Setup backend

The authorization backend accepts a standard Jam configuration as its configuration:

* `config`: `str | dict[str, Any] | None = None` - [Standard Jam configuration](/configuration).
* `pointer`: `str` - [Pointer](/configuration/#pointer-str-jam) for config.
* other backend specific settings, see for each backend

```python
config = {
    "jwt": {
        "alg": "HS256",
        "secret": "SECRET"
    }
}

app = Starlette(
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=JWTBackend(
                config=config
            ),
        )
    ]
)
```

## Users

In Starlette, [user classes](https://starlette.dev/authentication/#users) included in the `request` are used for authentication. Jam also uses this concept to facilitate integration.

### Create user model

Users are created using the abstract `base_user` class, in which you must implement the `from_payload` `classmethod`, which takes data from a token or session as input and converts it into a class:

```python
from jam.ext.starlette import BaseUser

# Let's say we're using a payload
# like this for authentication:
example_payload = {
    "id": 123
    "username": "some_username",
    "role": "role"
}

# Create your own user
@dataclass
class MyUser(BaseUser):
    id: int
    username: str
    role: str
    
    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "MyUser":
        return cls(
            id=payload["id"],
            username=payload["username"],
            role=payload["role"],
        )

app = Starlette(
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=JWTBackend(
                config=config,
                user_class=MyUser,
            ),
        )
    ]
)
```
After that, we can use this user directly from `request`:

```python
async def get_username(request: Request) -> str | None:
    if request.user.is_authenticated:
        return request.user.name
    else:
        return None
```

### Simple user
If you don't need complex user logic, you can use the `SimpleUser` class. It's a class with a single attribute, `payload`: `dict[str, Any]`, which holds the entire payload.

Example:

```python
from jam.ext.starlette import SimpleUser

async def get_payload(request: Request) -> dict | None:
    if not request.user.is_authenticated:
        return None
    else:
        return request.user.payload
        
app = Starlette(
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=JWTBackend(
                config=config,
                user_class=SimpleUser,
            ),
        )
    ]
)
```

## JWT Backend

Module: `jam.ext.starlette.JWTBackend`

Args:

* `config`: `str | dict[str, Any] | None = None` - Jam config
* `pointer`: `str` - Config pointer
* `cookie_name`: `str | None = None` - Cookie to check
* `header_name`: `str | None = None` - Header to check
* `bearer`: `bool = False` - Use bearer prefix for token (e.g. "Bearer ")
* `use_list`: `bool = False` - Use token black/white list
* `user`: `type[BaseUser] = SimpleUser` - User for request

```python
from jam.ext.starlette import JWTBackend


app = Starlette(
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=JWTBackend(
                config="config.toml",
                cookie_name="jwt"
            ),
        )
    ]
)
```

## PASETO Backend

Module: `jam.ext.starlette.PASETOBackend`

Args:

* `config`: `str | dict[str, Any] | None = None` - Jam config
* `pointer`: `str` - Config pointer
* `cookie_name`: `str | None = None` - Cookie to check
* `header_name`: `str | None = None` - Header to check
* `bearer`: `bool = False` - Use bearer prefix for token (e.g. "Bearer ")
* `user`: `type[BaseUser] = SimpleUser` - User for request

```python
from jam.ext.starlette import PASETOBackend


app = Starlette(
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=PASETOBackend(
                config="config.toml",
                header_name="Authorization"
            ),
        )
    ]
)
```

## Server side sessions backend

Module: `jam.ext.starlette.SessionBackend`

Args:

* `config`: `str | dict[str, Any] | None = None` - Jam config
* `pointer`: `str` - Config pointer
* `cookie_name`: `str | None = None` - Cookie to check
* `header_name`: `str | None = None` - Header to check
* `bearer`: `bool = False` - Use bearer prefix for token (e.g. "Bearer ")
* `user`: `type[BaseUser] = SimpleUser` - User for request

```python
from jam.ext.starlette import SessionBackend


app = Starlette(
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=JWTBackend(
                config="config.toml",
                cookie_name="sessionId"
            ),
        )
    ]
)
```
