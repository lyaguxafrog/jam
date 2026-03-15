---
title: Home
image: assets/logo_n_title.png
---
<div style="text-align: center;">
    <img alt="logo" src="assets/loog_n_title.png" />
    <p>Welcome to Jam documentation!</p>
</div>

![Python Version](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
[![PyPI - Version](https://img.shields.io/pypi/v/jamlib)](https://pypi.org/project/jamlib/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/jamlib?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=RED&left_text=Downloads)](https://pypi.org/project/jamlib/)
![tests](https://github.com/lyaguxafrog/jam/actions/workflows/run-tests.yml/badge.svg)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/lyaguxafrog/jam)
[![GitHub License](https://img.shields.io/github/license/lyaguxafrog/jam)](https://github.com/lyaguxafrog/jam/blob/master/LICENSE.md)

## About
Jam(Jeneric auth module) - a simple library that makes implementing authentication in your application effortless.

## Installation
<!-- termynal -->
```
> pip install jamlib
---> 100%
Installed!
```


## Quick example
```python
from jam import Jam

jam = Jam(config="config.toml")
payload = {
    "user": 1
}

jwt = jam.jwt_create(payload)
session_id = jam.session_create("user@mail.com", payload)
otp_code = jam.otp_code(secret="7K2HVNA3IQCYFFDX76IXKNCZHQ")
```

## Asynchronous support
!!! note
    You can use `jam.aio` module to work with async functions. **The methods are the same**, but you need to use `await` keyword.


```python
from jam.aio import Jam

jam = Jam()
payload = await jam.jwt_make_payload(
    exp=3600, data={"user_id": 1}
)
token = await jam.jwt_create(payload)
```


## Why Jam?
Jam is a library that provides the most popular AUTH* mechanisms right out of the box.

* [JWT](usage/jwt.md)
* [PASETO](usage/paseto.md)
* [Server side sessions](usage/sessions.md)
* [OTP](usage/otp.md)
* [OAuth2](usage/oauth2.md)


### Framework integrations

Jam provides ready-to-use integrations for the most popular frameworks:

* [FastAPI](framework_integrations/fastapi.md)
* [Starlette](framework_integrations/starlette.md)
* [Litestar](framework_integrations/litestar.md)
* [Flask](framework_integrations/flask.md)

Each integration offers built-in middleware or plugin support for JWT and session-based authentication.

### Why choose Jam?
Jam supports many authentication methods out of the box with minimal dependencies.
Here is a comparison with other libraries:

| Features / Library    | **Jam** | [Authx](https://authx.yezz.me/) | [PyJWT](https://pyjwt.readthedocs.io) | [AuthLib](https://docs.authlib.org) | [OTP Auth](https://otp.authlib.org/) |
|-----------------------|--------|----------------------------------|---------------------------------------|-------------------------------------|--------------------------------------|
| JWT                   | ✅     | ✅                               | ✅                                    | ✅                                  | ❌                                   |
| JWT black/white lists | ✅     | ❌                               | ❌                                    | ❌                                  | ❌                                   |
| PASETO                | ✅     | ❌                               | ❌                                    | ❌                                  | ❌                                   |
| Server side sessions  | ✅     | ✅                               | ❌                                    | ❌                                  | ❌                                   |
| OTP                   | ✅     | ❌                               | ❌                                    | ❌                                  | ✅                                   |
| OAuth2                | ✅     | ✅                               | ❌                                    | ✅                                  | ❌                                   |
| Flexible config       | ✅     | ❌                               | ❌                                    | ❌                                  | ❌                                   |
| Modularity            | ✅     | ❌                               | ❌                                    | ❌                                  | ❌                                   |
