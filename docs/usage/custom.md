---
title: Custom modules
---

You can easily override the implementation of any module using the `Base*` class. For example, if we want to override the implementation of the JWT module, we use `jam.jwt.BaseJWT`:

```python
from jam import Jam
from jam.jwt import BaseJWT

class MyJWT(BaseJWT):
    def __init__(
        self,
        secret_key: str,
    ):
        self.secret_key = secret_key
        
    def encode(self, payload: dict) -> str:
        # your logic
        return token
        
    def decode(self, token: str) -> dict:
        # your logic
        return payload


config = {
    "jwt": {
        "secret_key": "secret",
    }
}

Jam.MODULES["jwt"] = "path.to.MyJWT"
jam = Jam(config=config)

token = jam.jwt_create(payload={"user_id": 123})
```

You can also replace modules within framework integrations.
For example, suppose you want to replace the `JWT` implementation module in the [Starlette integration](http://127.0.0.1:8000/framework_integrations/starlette/):

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from jam.ext.starlette import JWTBackend
from jam.jwt import BaseJWT

class MyJWT(BaseJWT):
    def __init__(
        self,
        secret_key: str,
    ):
        self.secret_key = secret_key
        
    def encode(self, payload: dict) -> str:
        # your logic
        return token
        
    def decode(self, token: str) -> dict:
        # your logic
        return payload

JWTBackend.MODULE = MyJWT

app = Starlette(
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=JWTBackend(config="config.toml")
        ),
    ],
)
```
