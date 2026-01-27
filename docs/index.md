---
title: Home
image: assets/logo_n_title.png
---
<div style="text-align: center;">
    <img alt="logo" src="assets/loog_n_title.png" />
    <p>Welcome to Jam documentation!</p>
</div>

## About
Jam(Jeneric auth module) - a simple library that makes implementing authentication in your application effortless.

## Installation
<!-- termynal -->
```
> pip install jamlib
---> 100%
Installed!
```
How to install dev version: -> [Jam Unstable](install_unstable.md)

## Asynchronous support
!!! note
    You can use `jam.aio` module to work with async functions. **The methods are the same**, but you need to use `await` keyword.


```python
from jam.aio import Jam


jam = Jam()
payload = await jam.jwt_make_payload(**{"user_id": 1})
token = await jam.jwt_create_token(payload)
```


## Why Jam?
Jam is a library that provides the most popular AUTH* mechanisms right out of the box.

* [JWT](jwt/instance.md)
* [PASETO](paseto/instance.md)
* [Server side sessions](sessions/instance.md)
* OTP
    * [TOTP](otp/totp.md)
    * [HOTP](otp/hotp.md)
* [OAuth2](oauth2/instance.md)


### Framework integrations

Jam provides ready-to-use integrations for the most popular frameworks:

* [FastAPI](extensions/fastapi.md)
* [Starlette](extensions/starlette.md)
* [Litestar](extensions/litestar.md)
* [Flask](extensions/flask.md)

Each integration offers built-in middleware or plugin support for JWT and session-based authentication.

### Why choose Jam?
Jam supports many authentication methods out of the box with minimal dependencies.
Here is a comparison with other libraries:

| Features / Library    | **Jam**                                                                                              | [Authx](https://authx.yezz.me/) | [PyJWT](https://pyjwt.readthedocs.io) | [AuthLib](https://docs.authlib.org) | [OTP Auth](https://otp.authlib.org/) |
|-----------------------|------------------------------------------------------------------------------------------------------|--------------------------------|---------------------------------------|-------------------------------------|--------------------------------------|
| JWT                   | ✅                                                                                                    | ✅ | ✅ | ✅ | ❌                                    |
| JWT black/white lists | ✅                                                                                                    | ❌ | ❌ | ❌ | ❌ |
| Server side sessions  | ✅                                                                                                    | ✅ | ❌ | ❌ | ❌                                    |
| OTP                   | ✅                                                                                                    | ❌ | ❌ | ❌ | ✅ |
| OAuth2                | ✅                                                                                                     | ✅ | ❌ | ✅ | ❌ |
| Flexible config       | ✅                                                                                                    | ❌ | ❌ | ❌ | ❌ |
| Modularity            | ✅                                                                                                    | ❌ | ❌ | ❌ | ❌ |
