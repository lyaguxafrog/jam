---
title: "Jam + Starlette = <3"
---

The extension with Starlette is implemented
by `AuthBackend`'s for `AuthenticationMiddleware`.

For more detailed information about `AuthBackend`, `AuthMiddleware`,
and auth* in Starlette in general, see the [official documentation](https://starlette.dev/authentication/).   

## JWTBackend
For jwt auth*, `jam.ext.starlette.JWTBackend` is used,
which needs to be integrated into the standard `AuthenticationMiddleware`:

```python
Middleware(
    AuthenticationMiddleware,
    backend=JWTBackend(jam, cookie_name, header_name)
)
```
### Middleware set
Three parameters must be passed to `JWTBackend`:

#### `jam`: `BaseJam`
Jam instance.

#### `cookie_name`: `str | None`
The cookie name for the access token. If passed, `Middleware` will
read the token from it. If `None` is passed, `Middleware` will read the `header`.

#### `header_name`: `str | None`

The name of the header for the access token. If passed, `Middleware` will
read the token from the header. If `None` is passed, `Middleware` will read the `cookie`.

!!! tip
    `JWTBackend` expects the header to be in the format: `Bearer <token>`


```python

jam = Jam()
app = Starlette(
    routes=routes,
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=JWTBackend(
                jam=jam,
                cookie_name="jwt",
                header_name=None
            )
        )
    ]
)
```

After that, if the user has been authorized, their
payload can be obtained using `request.user.payload`:
```python
def get_user(request: Request) -> Response:
    user_payload = request.user.payload
    # another logic
```

### Usage example
```python
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import Response
from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from jam import Jam
from jam.ext.starlette import JWTBackend

jam = Jam()

def login() -> Response:
    # login logic
    payload = jam.make_payload(**{"user": 1})
    token = jam.gen_jwt_token(payload)
    response = Response(token)
    response.set_cookie("jwt", token)
    return response

def get_user(request: Request) -> Response:
    user_payload = request.user.payload
    return Response(user_payload)


app = Starlette(
    routes=[
        Route("/login", login),
        Route("/user", get_user)  
    ],
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=JWTBackend(
                jam=jam,
                cookie_name="jwt",
                header_name=None
            )
        )
    ]
)
```

---
## SessionBackend
For sessions auth*, `jam.ext.starlette.SessionBackend`is used,
which needs to be integrated into the standard AuthenticationMiddleware:
```python
Middleware(
    AuthenticationMiddleware,
    backend=SessionBackend(jam, cookie_name, header_name)
)
```

### Middleware set
Three parameters must be passed to SessionBackend:

#### `jam`: `BaseJam`
The created Jam instance.

#### `cookie_name`: `str | None`
The cookie name for the session id.
If passed, `Middleware` will read the session id from it.
If `None` is passed, `Middleware` will read the header.

#### `header_name`: `str | None`
The name of the header for the session id.
If passed, `Middleware` will read the session id from the header.
If `None` is passed, `Middleware` will read the cookie.

!!! tip
    `SessionBackend` expects the header to be in the format: `Bearer <session_id>`

```python
jam = Jam()
app = Starlette(
    routes=routes,
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=SessionBackend(
                jam=jam,
                cookie_name="sessionId",
                header_name=None
            )
        )
    ]
)
```

After that, if the user has been authorized, their payload can be obtained using `request.user.payload`:
```python
def get_user(request: Request) -> Response:
    user_payload = request.user.payload
    # another logic
```

### Usage example
```python
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import Response
from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from jam import Jam
from jam.ext.starlette import SessionBackend

jam = Jam()

def login() -> Response:
    # login logic
    session_id = jam.create_session("username", {"user": 1})
    response = Response(session_id)
    response.set_cookie("sessionId", session_id)
    return response

def get_user(request: Request) -> Response:
    user_payload = request.user.payload
    return Response(user_payload)


app = Starlette(
    routes=[
        Route("/login", login),
        Route("/user", get_user)  
    ],
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=SessionBackend(
                jam=jam,
                cookie_name="jwt",
                header_name=None
            )
        )
    ]
)
```
