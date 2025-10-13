---
title: "Jam + Litestar = <3"
---

Integration with Litestar is implemented by [plugins](https://docs.litestar.dev/2/usage/plugins/index.html).

## Jam Plugin

This is a simple plugin that does not check tokens/sessions
like `JWTPlugin` and `SessionPlugin`. It is needed for easy access to
jam inside routes, via Litestar DI:

!!! note
    Litestar automatically injects plugin-provided dependencies into route handlers via its dependency injection (DI) system.

!!! tip
    For more convenient operation, it is recommended to use
    `JamPlugin` in conjunction with other plugins,
    for example `JamPlugin` + `JWTPlugin`.

```python
@get(path="/login")
async def login(logindto: LoginDTO, jam: Jam) -> bool:
    # some logic
    payload = jam.make_payload(**{"user": 1})
    token = jam.gen_jwt_token(payload)
    return True
```

Example of integration with your Litestar application:
```python
from litestar import Litestar

from jam import Jam
from jam.ext.litestar import JamPlugin


jam = Jam()
app = Litestar(
    plugins=[JamPlugin(jam)]
)
```
---
## JWT Plugin

This plugin creates [`Middleware`](/api/ext/litestar/middlewares/#jam.ext.litestar.middlewares.JamJWTMiddleware) that checks tokens in
cookies/headers and passes the payload to `Request`.

### Setup plugin

#### `jam`: `BaseJam`
Jam instance

#### `cookie_name`: `str | None`
The cookie name for the access token.
If passed, plugin will read the token from it.
If `None` is passed, plugin will read the header.

#### `header_name`: `str | None`
The name of the header for the access token.
If passed, plugin will read the token from the header.
If `None` is passed, plugin will read the cookie.

!!! tip
    `JWTPlugin` expects the header to be in the format: `Bearer <token>`

```python
from litestar import Litestar

from jam import Jam
from jam.ext.litestar import JWTPlugin

jam = Jam()
app = Litestar(
    plugins=[JWTPlugin(jam=jam, cookie_name="jwt", header_name=None)]
)
```
After that, if the user has been authorized,
their payload can be obtained using `request.user.payload`:
```python
@get(path="/user")
async def user(request: Request) -> str:
    payload = request.user.payload
    return str(payload)
```

### Usage example
```python
from litestar import Litestar, get, post, Request, Response
from litestar.openapi.spec import Components, SecurityScheme

from jam.ext.litestar import JWTPlugin
from jam import Jam


jam = Jam()

@post(path="/auth")
async def auth(username: str, password: str) -> Response:
    # some logic
    payload = jam.make_payload(**{"user": 1})
    
    token = jam.gen_jwt_token(payload)
    response = Response({"token": token})
    response.set_cookie("jwt", token)
    return response


@get(path="/user")
async def user(request: Request) -> str:
    payload = request.user.payload
    return str(payload)


app = Litestar(
    debug=True,
    route_handlers=[auth, user],
    plugins=[
        JWTPlugin(jam=jam, cookie_name="jwt", header_name=None)
    ]
)
```

---
## Sessions Plugin

This plugin creates [`Middleware`](/api/ext/litestar/middlewares/#jam.ext.litestar.middlewares.JamSessionsMiddleware) that checks sessions ids in
cookies/headers and passes the payload to `Request`.

### Setup plugin

#### `jam`: `BaseJam`
Jam instance

#### `cookie_name`: `str | None`
The cookie name for the session id.
If passed, plugin will read the session id from it.
If `None` is passed, plugin will read the header.

#### `header_name`: `str | None`
The name of the header for the session id.
If passed, plugin will read the session id from the header.
If `None` is passed, plugin will read the cookie.

!!! tip
    `SessionPlugin` expects the header to be in the format: `Bearer <token>`

```python
from litestar import Litestar

from jam import Jam
from jam.ext.litestar import SessionsPlugin

jam = Jam()
app = Litestar(
    plugins=[SessionsPlugin(jam=jam, cookie_name="sessionId", header_name=None)]
)
```
After that, if the user has been authorized,
their payload can be obtained using `request.user.payload`:
```python
@get(path="/user")
async def user(request: Request) -> str:
    payload = request.user.payload
    return str(payload)
```

### Usage example
```python
from litestar import Litestar, get, post, Request, Response
from litestar.openapi.spec import Components, SecurityScheme

from jam.ext.litestar import SessionsPlugin
from jam import Jam


jam = Jam()

@post(path="/auth")
async def auth(username: str, password: str) -> Response:
    # some logic
    session_id = jam.create_session("username", {"user": 1})
    response = Response({"sessionId": session_id})
    response.set_cookie("sessionId", session_id)
    return response


@get(path="/user")
async def user(request: Request) -> str:
    payload = request.user.payload
    return str(payload)


app = Litestar(
    debug=True,
    route_handlers=[auth, user],
    plugins=[
        SessionsPlugin(jam=jam, cookie_name="sessionId", header_name=None)
    ]
)
```