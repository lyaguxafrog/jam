---
title: JOSE
---

!!! tip
    The old JWT method has been deprecated and will be removed in Jam 4.0.0. We strongly recommend switching to the new implementation. However, the old documentation is still available: [`jam.makridenko.ru/usage/jwt/`](/usage/jwt/)

## JWT

### Use in instance

#### Config

* `alg`: `str` - Algorithm for generating JWT tokens. Supports: `HS256`, `HS384`, `HS512`, `RS256`, `RS384`, `RS512`, `ES256`, `ES384`, `ES512`, `PS256`, `PS384`, `PS512`.
* `secret`: `str` - Secret key for token signing. By default, Jam reads the environment variable `JAM_JWT_SECRET_KEY`.
* `list`: `dict[str, str] | None = None` - Token black/white list config. See: `jam.jose.list`.

```toml
[jam.jose.jwt]
alg = "RS256"
secret = "$RS_PRIVATE_KEY"

[jam.jose.jwt.list]
type = "black"
backend = "redis"
redis_uri = "redis://localhost:6379"
```

### Usage

```python
from jam import Jam

jam = Jam(config="config.toml")
```

#### Encode JWT

Method: `jam.jwt_encode`

Args:

* `iss`: `str | None = None` - Token issuer.
* `sub`: `str | None = None` - Token subject.
* `aud`: `str | None = None` - Token audience.
* `exp`: `int | None = None` - Token expiration time in seconds.
* `nbf`: `int | None = None` - Token not-before time in seconds.
* `jti`: `str | None = None` - Token JWT ID. If `none` use the JTI fabric function.
* `payload`: `dict[str, Any] | None = None` -  The payload to include in the JWT.
* `header`: `dict[str, Any] | None = None` - The header to include in the JWT.

Returns:

`srt`: JWT

```python
token = jam.jwt_encode(
    iss="YourService",
    sub="user@mail.com",
)
```

#### Decode token

Method: `jam.jwt_decode`

Args:

* `token`: `str` - JWT.
* `check_exp`: `bool = True` - Check expire.
* `check_list`: `bool = True` - Check white/black lists.
* `check_nbf`: `bool = False` - Check not-before time.
* `include_headers`: `bool = False` - Include headers in the decoded payload

Returns:

`dict[str, Any]`: Decoded payload or payload+header.

```python
data = jam.jwt_decode(
    token=my_jwt,
    check_exp=True,
    check_list=False,
    check_nbf=True
)
```

### Use out of instance

#### Built

Module: `jam.jose.JWT`

Args:

* `alg`: `str | None` - JWT algorithm name for signing (JWS). Used if jws is not provided.
* `enc`: `str | None` - JWE content encryption algorithm. If provided, creates encrypted JWT.
* `secret_key`: `str | bytes | KeyLike | JWK | None` - Key for signing/encryption.
* `password`: `str | bytes | None` - Password for encrypted private keys.
* `list`: `dict[str, Any] | None` - List config for token storage.
* `serializer`: `BaseEncoder | type[BaseEncoder]` - JSON encoder/decoder.
* `logger`: `BaseLogger` - Logger instance.
* `jws`: `JWS | None` - Pre-built JWS instance. If provided, alg is ignored.
* `jwe`: `JWE | None` - Pre-built JWE instance. If provided, enc and secret_key are ignored.

```python
import os
from jam.jose import JWT

jwt = JWT(
    alg="RSA256",
    secret_key=os.getenv("RS_PRIVATE_KEY")
)
```

#### Create JTI
Method: `JWT.jti`

Returns: `str`: New JTI

```
jti = jwt.jti
```


#### Encode token
Method: `jwt.encode`

Args:

* `exp`: `int | None` - The expiration time in seconds.
* `nbf`: `int | None` - The not-before time in seconds.
* `iss`: `str | None` - The issuer.
* `sub`: `str | None` - The subject.
* `aud`: `str | None` - The audience.
* `jti`: `str | None` - The JWT ID.
* `header` `dict[str, Any] | None` - The header to include in the JWT.
* `payload`: `dict[str, Any] | None` - The payload to include in the JWT.

Returns: `str` - The encoded JWT.
