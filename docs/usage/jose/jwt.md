---
title: JWT
---

!!! tip
    The `jam.jwt` module is [deprecated](/breaking_changes/deprecated), but the documentation is still available at [/usage/jwt](/usage/jwt)

## Instance (jam.Jam)

### Config

```toml
[jam.jose.jwt]
alg = "RS256"
secret = "$RSA_PRIVATE_KEY"

[jam.jose.jwt.list]
type = "black"
backend = "redis"
redis_uri = "redis://localhost:6379"
```

Args:

* `alg`: `str` - JWT signing algorithm. Supports: `HS256`, `HS384`, `HS512`, `RS256`, `RS384`, `RS512`, `ES256`, `ES384`, `ES512`, `PS256`, `PS384`, `PS512`.
* `secret`: `str` - Secret key for token signing. Default reads from `JAM_JWT_SECRET_KEY` environment variable.
* `list`: `dict[str, Any] | None` - Token list config. See: [Lists](lists.md).

### Usage

```python
from jam import Jam

jam = Jam(config="config.toml")
```

### Encode token

Method: `jam.jwt_encode`

Args:

* `iss`: `str | None = None` - Token issuer.
* `sub`: `str | None = None` - Token subject.
* `aud`: `str | None = None` - Token audience.
* `exp`: `int | None = None` - Token lifetime in seconds.
* `nbf`: `int | None = None` - Token not-before time in seconds.
* `jti`: `str | None = None` - Unique token ID. If `None`, auto-generated.
* `header`: `dict[str, Any] | None = None` - Additional header fields.
* `payload`: `dict[str, Any] | None = None` - Custom payload data.

Returns:

`str`: Encoded JWT.

```python
token = jam.jwt_encode(
    iss="YourService",
    sub="user@mail.com",
    exp=3600,
    payload={"role": "admin"}
)
print(token)
>>> eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQ...
```

### Decode token

Method: `jam.jwt_decode`

Args:

* `token`: `str` - JWT token.
* `validate_claims`: `bool = True` - Validate exp and nbf claims.

Returns:

`dict[str, Any]`: Decoded payload with header.

Raises:

* `JamJWTExpired` - Token has expired.
* `JamJWTNotYetValid` - Token is not yet valid (nbf).
* `JamJWSVerificationError` - Invalid signature.

```python
data = jam.jwt_decode(
    token=token,
    validate_claims=True
)
print(data)
>>> {
    'header': {'alg': 'RS256', 'typ': 'JWT'},
    'payload': {
        'iss': 'YourService',
        'sub': 'user@mail.com',
        'exp': 1772132706,
        'iat': 1772129106,
        'jti': '0c2c38d2-5dcb-4294-bb2d-0820f6ff787d',
        'role': 'admin'
    }
}
```

### Encrypt token

Method: `jam.jwt_encrypt`

Creates encrypted JWT (JWS+JWE or JWE only).

Args:

* `payload`: `dict[str, Any] | str` - Data to encrypt.
* `header`: `dict[str, Any] | None = None` - Additional JWE header fields.

Returns:

`str`: Encrypted JWT.

```python
encrypted = jam.jwt_encrypt(
    payload={"user_id": 123, "role": "admin"},
    header={"custom": "value"}
)
print(encrypted)
>>> eyJhbGciOiJSU0ExLjI1NiIsImVuYyI6IkExMjhHQ1Mtc2hhMjU2In0...
```

### Decrypt token

Method: `jam.jwt_decrypt`

Decrypts encrypted JWT.

Args:

* `token`: `str` - Encrypted JWT token.

Returns:

`dict[str, Any]`: Decrypted payload.

Raises:

* `JamJWEDecryptionError` - Decryption failed.

```python
data = jam.jwt_decrypt(token=encrypted)
print(data)
>>> {'user_id': 123, 'role': 'admin'}
```

## Standalone (module)

### Create instance

Module: `jam.jose.JWT`

Args:

* `alg`: `str | None` - Signing algorithm (JWS).
* `enc`: `str | None` - Content encryption algorithm (JWE). Creates encrypted JWT if specified.
* `secret_key`: `str | bytes | KeyLike | JWK | None` - Key for signing/encryption.
* `password`: `str | bytes | None` - Password for encrypted private keys.
* `list`: `dict[str, Any] | None` - Token list config.
* `serializer`: `BaseEncoder | type[BaseEncoder] = JsonEncoder` - JSON encoder/decoder.
* `logger`: `BaseLogger` - Logger instance.
* `jws`: `JWS | None` - Pre-built JWS instance. If provided, alg is ignored.
* `jwe`: `JWE | None` - Pre-built JWE instance. If provided, enc and secret_key are ignored.

```python
import os
from jam.jose import JWT

jwt = JWT(
    alg="RS256",
    secret_key=os.getenv("RSA_PRIVATE_KEY")
)
```

### Encode token

Method: `jwt.encode`

Args:

* `iss`: `str | None = None` - Issuer.
* `sub`: `str | None = None` - Subject.
* `aud`: `str | None = None` - Audience.
* `exp`: `int | None = None` - Lifetime in seconds.
* `nbf`: `int | None = None` - Not-before in seconds from now.
* `jti`: `str | None = None` - JWT ID.
* `header`: `dict[str, Any] | None = None` - Additional header.
* `payload`: `dict[str, Any] | None = None` - Custom data.

Returns:

`str`: Encoded JWT.

```python
token = jwt.encode(
    exp=3600,
    sub="user@email.com",
    payload={"user_id": 123}
)
```

### Decode token

Method: `jwt.decode`

Args:

* `token`: `str` - JWT token.
* `validate_claims`: `bool = True` - Validate exp/nbf.

Returns:

`dict[str, dict[str, Any]]`: Dict with `header` and `payload` keys.

Raises:

* `JamJWTExpired` - Token expired.
* `JamJWTNotYetValid` - Token not yet valid.
* `JamJWSVerificationError` - Invalid signature or token type.

```python
data = jwt.decode(token, validate_claims=True)
print(data["payload"]["sub"])
>>> "user@email.com"
```

### Encrypt token

Method: `jwt.encrypt`

Args:

* `payload`: `dict[str, Any] | str` - Data to encrypt.
* `header`: `dict[str, Any] | None = None` - Additional header.

Returns:

`str`: Encrypted JWT.

```python
encrypted = jwt.encrypt(
    payload={"data": "sensitive"},
    header={"purpose": "auth"}
)
```

### Decrypt token

Method: `jwt.decrypt`

Args:

* `token`: `str` - Encrypted JWT.

Returns:

`dict[str, Any]`: Decrypted data.

```python
data = jwt.decrypt(token=encrypted)
print(data)
>>> {"data": "sensitive"}
```

### Generate JTI

Property: `jwt.jti`

Returns:

`str`: Unique UUID for JWT ID.

```python
jti = jwt.jti
print(jti)
>>> "0c2c38d2-5dcb-4294-bb2d-0820f6ff787d"
```

## Error handling

```python
from jam import Jam
from jam.exceptions import (
    JamJWTExpired,
    JamJWTNotYetValid,
    JamJWSVerificationError,
)

jam = Jam(config="config.toml")

try:
    data = jam.jwt_decode(token=token, validate_claims=True)
except JamJWTExpired:
    print("Token has expired")
except JamJWTNotYetValid:
    print("Token is not yet valid")
except JamJWSVerificationError:
    print("Invalid signature")
```
