## JWT

```python
from fastapi import FastAPI
from jam import Jam


config = {
    "auth_type": "jwt",
    "secret_key": "SECRET"
}

app = FastAPI()
jam = Jam(config)


@app.post(
    path="/user/auth"
)
async def auth_user(username: str, password: str) -> str:
    token = jam.gen_jwt_token({"username": username})
    return token

@app.get(
    path="/user"
)
async def get_user(token: str) -> str:
    payload = jam.verify_jwt_token(token, False, False)
    return payload["username"]
```

## Sessions
```python
from fastapi import FastAPI
from jam import Jam

config = {
    "auth_type": "session",
    "session_type": "redis",
    "is_session_crypt": False,
    "redis_uri": "redis://0.0.0.0:6379/0"
}

app = FastAPI()
jam = Jam(config)


@app.post(
    path="/user/auth"
)
async def auth_user(username: str, password: str) -> str:
    session_id = jam.create_session(
        session_key=username,
        data={
            "username": username,
            "another": "data"
        }
    )
    return session_id

@app.get(
    path="/user"
)
async def get_user(session_id: str) -> str:
    data = jam.get_session(session_id)
    return data["username"]
```