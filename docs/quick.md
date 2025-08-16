# Quick

Sometimes it's not always convenient to use instance-class, so Jam has quick commands to work with auth.

## JWT
```python
from jam.quick import (
    get_jwt_token, decode_jwt_token, verify_jwt_token    
)

token: str = get_jwt_token(
    alg="HS256",
    payload={"user_id": 1},
    secret_key="SOME_KEY"
)

payload: dict[str, Any] = decode_jwt_token(
    token=token,
    secret_key="SOME_KEY"
)

result: bool = verify_jwt_token(
    token=token,
    secret_key="SOME_KEY"
)

# async version

from jam.quick import (
    aget_jwt_token, adecode_jwt_token, averify_jwt_token
)

token: str = await aget_jwt_token(
    alg="HS256",
    payload={"user_id": 1},
    secret=key="SOME_KEY"
)

payload: dict[str, Any] = await adecode_jwt_token(
    token=token,
    secret_key="SOME_KEY"
)

result: bool = await averify_jwt_token(
    token=token,
    secret_key="SOME_KEY"
)
```
See [API/jam.quick/jwt](api/quick/jwt.md) for more details.