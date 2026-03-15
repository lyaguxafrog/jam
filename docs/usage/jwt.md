---
title: JWT
---

## Use in instance

### Config

* `alg`: `str` - Algorithm for generating JWT tokens. Supports: `HS256`, `HS384`, `HS512`, `RS256`, `RS384`, `RS512`, `ES256`, `ES384`, `ES512`, `PS256`, `PS384`, `PS512`.
* `secret_key`: `str` - Secret key for token signing. By default, Jam reads the environment variable `JAM_JWT_SECRET_KEY`.
* `password`: `str` - Password for encrypted private keys.
* `list`: `dict[str, Any] | None = None` - Token black/white list config. See: [`jam.jwt.list`](/api/jam.jwt.lists/).


```toml
[jam.jwt]
alg = "HS256"
secret_key = "YOURSECRETKEY"
password = "PASSWORD_FOR_PRIVATE_KEY"

[jam.jwt.list]
type = "black"
backend = "redis"
redis_uri = "redis://localhost:6379"
```

### Usage

```python
from jam import Jam

jam = Jam(config="config.toml")
```

#### Generate payload

Method: `jam.jwt_make_payload`

Args:

* `exp`: `int | None` - Token life time.
* `data`: `dict[str, Any]` - Custom data.

Returns:

`dict[str, Any]`: Payload for token.

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

* `payload`: `dict[str, Any]` - Payload for token.

Returns:

`str`: Token.

```python
token = jam.jwt_create(payload=payload)
print(token)
>>> eyJhbGciOiAi...
```

#### Decode token

Method: `jam.jwt_decode`

Args:

* `token`: `str` - Token to decode.
* `check_exp`: `bool` - Check token expiration.
* `check_list`: `bool` - Check token black/white list.

Returns:

`dict[str, Any]`: Decoded token data.

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

#### List

Method: `jam.jwt.list`


##### Add token to list

Method: `jam.jwt.list.add`

Args:

* `token`: `str` - Token to add.

```python
jam.jwt.list.add(
    token=token
)
```

##### Remove token from list

Method: `jam.jwt.list.delete`

Args:

* `token`: `str` - Token to remove.

```python
jam.jwt.list.remove(
    token=token
)
```

##### Check token in list

Method: `jam.jwt.list.check`

Args:

* `token`: `str` - Token to check.

Returns:

`bool`: `True` if token is in list, `False` otherwise.

```python
result = jam.jwt.list.check(
    token=token
)
print(result)
>>> False
```


## Use out of instance

### Built

Module: `jam.jwt.JWT`

Args:

* `alg`: `str` - Algorithm for token generation.
* `secret_key`: `str | bytes` - Secret key for token generation. By default, Jam reads the environment variable `JAM_JWT_SECRET_KEY`.
* `password`: `str | bytes | None` - Password for token generation.
* `list`: `dict[str, Any] | None` - List config. See: [`jam.jwt.list`](/api/jam.jwt.lists/).

```python
from jam.jwt import JWT

jwt = JWT(
    alg="HS256",
    secret_key="SECRET_KEY",
    password=None,
    list={
        "type": "black",
        "backend": "json",
        "json_path": "lists.json"
    }
)
```

### Encode token

Method: `JWT.encode`

Args:

* `payload`: `dict[str, Any]` - Payload for token.

Returns:

`str`: Token.

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

* `token`: `str` - Token to decode.
* `public_key`: `str | bytes | None` - Public key for token verification.

Returns:

`dict[str, Any]`: Decoded token data.

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

### List

Method: `JWT.list`

#### Add token to list

Method: `JWT.list.add`

Args:

* `token`: `str` - Token to add.

```python
jwt.list.add(token)
```

#### Remove token from list

Method: `JWT.list.delete`

Args:

* `token`: `str` - Token to remove.

```python
jwt.list.delete(token)
```

#### Check token in list

Method: `JWT.list.check`

Args:

* `token`: `str` - Token to check.

Returns:

`bool`: `True` if token is in list, `False` otherwise.

```python
result = jwt.list.check(token)
print(result)
>>> False
```
