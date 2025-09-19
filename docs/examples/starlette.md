## JWT (Starlette)

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from jam import Jam


config = {
    "auth_type": "jwt",
    "secret_key": "SECRET"
}

jam = Jam(config)


async def auth_user(request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    token = jam.gen_jwt_token({"username": username})
    return JSONResponse({"token": token})


async def get_user(request):
    token = request.query_params.get("token")
    payload = jam.verify_jwt_token(token, False, False)
    return JSONResponse({"username": payload["username"]})


routes = [
    Route("/user/auth", auth_user, methods=["POST"]),
    Route("/user", get_user, methods=["GET"]),
]

app = Starlette(routes=routes)
```

---

## Sessions

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from jam import Jam


config = {
    "auth_type": "session",
    "session_type": "redis",
    "is_session_crypt": False,
    "redis_uri": "redis://0.0.0.0:6379/0"
}

jam = Jam(config)


async def auth_user(request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    session_id = jam.create_session(
        session_key=username,
        data={
            "username": username,
            "another": "data"
        }
    )
    return JSONResponse({"session_id": session_id})


async def get_user(request):
    session_id = request.query_params.get("session_id")
    data = jam.get_session(session_id)
    return JSONResponse({"username": data["username"]})


routes = [
    Route("/user/auth", auth_user, methods=["POST"]),
    Route("/user", get_user, methods=["GET"]),
]

app = Starlette(routes=routes)
```