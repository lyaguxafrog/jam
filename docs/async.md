---
title: Async support
---

# Async support

Jam provides full async support through `jam.aio` module. The API is identical to the synchronous version, but methods that perform I/O operations use `async`/`await`.

## Instance

```python
from jam.aio import Jam

jam = Jam(config=config)
```

## Sessions

All session methods are async:

```python
# Create session
session_id: str = await jam.session_create(
    session_key="user", data={"user_id": 1}
)

# Get session
data: dict | None = await jam.session_get(session_id)

# Update session
await jam.session_update(session_id, {"role": "admin"})

# Delete session
await jam.session_delete(session_id)

# Clear all sessions
await jam.session_clear("user")

# Rework session
new_session_id: str = await jam.session_rework(session_id)
```

## OAuth2

All OAuth2 methods in `jam.aio.Jam` are async:

```python
# Get authorization URL (async for API consistency)
auth_url: str = await jam.oauth2_get_authorized_url(
    provider="github", scope=["user:email"]
)

# Fetch token (async)
token: dict = await jam.oauth2_fetch_token(
    provider="github", code="auth_code"
)

# Refresh token (async)
new_token: dict = await jam.oauth2_refresh_token(
    provider="github", refresh_token="refresh_token"
)

# Client credentials flow (async)
token: dict = await jam.oauth2_client_credentials_flow(
    provider="github", scope=["read"]
)
```

## JWT, OTP, PASETO

All JWT, OTP, and PASETO methods in `jam.aio.Jam` are async for API consistency, but internally use synchronous `jam.jwt`, `jam.otp`, and `jam.paseto` modules (no I/O operations):

```python
# JWT - async in jam.aio.Jam
payload = await jam.jwt_make_payload(exp=3600, data={"user_id": 1})
token = await jam.jwt_create_token(payload)
decoded = await jam.jwt_verify_token(token)

# OTP - async in jam.aio.Jam
code = await jam.otp_code(secret="secret")
is_valid = await jam.otp_verify_code(secret="secret", code=code)

# PASETO - async in jam.aio.Jam
payload = await jam.paseto_make_payload(exp=3600, data={"user_id": 1})
token = await jam.paseto_create(payload, footer=None)
decoded = await jam.paseto_decode(token)
```

## Direct module imports

When importing modules directly:

- **Async modules** (I/O operations): `jam.aio.sessions`, `jam.aio.oauth2`
- **Sync modules only** (no I/O): `jam.jwt`, `jam.otp`, `jam.paseto`

```python
# Async sessions module
from jam.aio.sessions import RedisSessions
session = RedisSessions(redis_uri="redis://...")
session_id = await session.create("user", {"data": 1})

# Sync JWT module (no jam.aio.jwt)
from jam.jwt import JWT
jwt = JWT(alg="HS256", secret="secret")
token = jwt.encode({"user_id": 1})  # synchronous
```

## Implementation details

- **Sessions**: `jam.aio.sessions` uses `redis.asyncio` for Redis and `asyncio.to_thread` for JSON
- **OAuth2**: `jam.aio.oauth2` uses `asyncio.to_thread` to wrap stdlib HTTP operations  
- **JWT/OTP/PASETO**: `jam.aio.Jam` methods are async for API consistency, but internally use synchronous `jam.jwt`, `jam.otp`, `jam.paseto` modules (no async module versions as they don't require I/O)
