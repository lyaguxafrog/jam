# Getting start

## Config

```python
from jam import Jam, Config

config: Config = Config(
    JWT_SECRET_KEY="super-secret-key",
    JWT_EXP=3600
)

jam: Jam = Jam(config=config)
```

## JWT

### Gen token

```python

payload: dict = {
    "id": 1,
    "role": "user"
}

token: str = jam.gen_token(payload=payload)
```

### Verify token

```python
payload: dict = jam.jwt_verify(token, secret)
```
