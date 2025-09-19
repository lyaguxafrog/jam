## JWT

```python
from litestar import Litestar, post, get
from litestar.response import Response
from jam import Jam


config = {
    "auth_type": "jwt",
    "secret_key": "SECRET"
}

jam = Jam(config)


@post("/user/auth")
async def auth_user(data: dict) -> Response:
    username = data.get("username")
    password = data.get("password")
    token = jam.gen_jwt_token({"username": username})
    return Response({"token": token})


@get("/user")
async def get_user(token: str) -> Response:
    payload = jam.verify_jwt_token(token, False, False)
    return Response({"username": payload["username"]})


app = Litestar(route_handlers=[auth_user, get_user])
```

## Sessions (Litestar)

```python
from litestar import Litestar, post, get
from litestar.response import Response
from jam import Jam


config = {
    "auth_type": "session",
    "session_type": "redis",
    "is_session_crypt": False,
    "redis_uri": "redis://0.0.0.0:6379/0"
}

jam = Jam(config)


@post("/user/auth")
async def auth_user(data: dict) -> Response:
    username = data.get("username")
    password = data.get("password")
    session_id = jam.create_session(
        session_key=username,
        data={
            "username": username,
            "another": "data"
        }
    )
    return Response({"session_id": session_id})


@get("/user")
async def get_user(session_id: str) -> Response:
    data = jam.get_session(session_id)
    return Response({"username": data["username"]})


app = Litestar(route_handlers=[auth_user, get_user])
```
