---
title: JWT
---

## Use in instance

### Config

* `alg`: `str` - Algorithm for generating JWT tokens. Supports: `HS256`, `HS384`, `HS512`, `RS256`, `RS384`, `RS512`, `ES256`, `ES384`, `ES512`, `PS256`, `PS384`, `PS512`
* `secret_key`: `str` - Secret key for token signing. By default, Jam reads the environment variable `JAM_JWT_SECRET_KEY`.
* `password`: `str` - Password for encrypted private keys.

```toml
[jam.jwt]
alg = "HS256"
secret_key = "YOURSECRETKEY"
password = "PASSWORD_FOR_PRIVATE_KEY"
```

### Usage

```python
from jam import Jam

jam = Jam(config="config.toml")
```

#### Generate payload

Method: `jam.jwt_make_payload`

Args:

* `exp`: `int | None` - Token life time
* `data`: `dict[str, Any]` - Custom data

Returns:

`dict[str, Any]`: Payload for token

```python
payload = jam.jwt_make_payload(
    exp=3600,
    data={
        "user": 1,
        "role": "admin"
    }
)
print(payload)
>>> {
        'iat': 1772116588.752527,
        'exp': 1772120188.752542,
        'jti': 'b3402bbc-d766-42bc-a763-3efc882dc540',
        'user': 1,
        'role': 'admin'
    }
```

#### Create token

Method: `jam.jwt_create`

Args:

* `payload`: `dict[str, Any]` - Payload for token

Returns:

`str`: Token

```python
token = jam.jwt_create(payload=payload)
print(token)
>>> eyJhbGciOiAi...
```

#### Decode token

Method: `jam.jwt_decode`

Args:

* `token`: `str` - Token to decode
* `check_exp`: `bool` - Check token expiration.
* `check_list`: `bool` - Check token black/white list.

Returns:

`dict[str, Any]`: Decoded token data

```python
data = jam.jwt_decode(
    token=token,
    check_exp=True,
    check_list=False
)
print(data)
>>> {
        'exp': 1772120451.373754,
        'iat': 1772116851.373746,
        'jti': '7cd12c49-2987-4011-8578-d3e7405d7673',
        'role': 'admin',
        'user': 1
    }
```

## Use out of instance

### Built

Module: `jam.jwt.JWT`

Args:

* `alg`: `str` - Algorithm for token generation.
* `secret_key`: `str | bytes` - Secret key for token generation. By default, Jam reads the environment variable `JAM_JWT_SECRET_KEY`.
* `password`: `str | bytes | None` - Password for token generation.

```python
from jam.jwt import JWT

jwt = JWT(
    alg="HS256",
    secret_key="SECRET_KEY",
    password=None
)
```

### Encode token

Method: `JWT.encode`

Args:

* `payload`: `dict[str, Any]` - Payload for token

Returns:

`str`: Token

```python
token = jwt.encode(
    payload={
        "id": 1
        "username": "lyaguxa"
    }
)
print(token)
>>> eyJhbGciOiAiSFM...
```

### Decode token

Method: `JWT.decode`

Args:

* `token`: `str` - Token to decode
* `public_key`: `str | bytes | None` - Public key for token verification

Returns:

`dict[str, Any]`: Decoded token data

```python
data = jwt.decode(
    token=token,
    public_key=None
)
print(data)
>>> {
        'id': 1,
        'username': 'lyaguxa'
    }
```
