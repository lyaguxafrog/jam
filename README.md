# Jam

![logo](https://github.com/lyaguxafrog/jam/blob/master/docs/assets/h_logo_n_title.png?raw=true)

![Python Version](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
[![PyPI - Version](https://img.shields.io/pypi/v/jamlib)](https://pypi.org/project/jamlib/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/jamlib?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=RED&left_text=Downloads)](https://pypi.org/project/jamlib/)
![tests](https://github.com/lyaguxafrog/jam/actions/workflows/run-tests.yml/badge.svg)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/lyaguxafrog/jam)
[![GitHub License](https://img.shields.io/github/license/lyaguxafrog/jam)](https://github.com/lyaguxafrog/jam/blob/master/LICENSE.md)

* Documentation: [jam.makridenko.ru](https://jam.makridenko.ru)
* Changelog: [CHANGELOG.md](https://github.com/lyaguxafrog/jam/blob/master/CHANGELOG.md)


## Install
```bash
pip install jamlib
```

## Quick example
```python
from jam import Jam

jam = Jam(config="config.toml")

jwt = jam.jwt_create({"user": 1})
session_id = jam.session_create(session_key="username", data={"user": 1})
otp_code = jam.otp_code(secret="3DB7FOAOFBCI3WFDRE7EPF43CA")
```

## Why Jam?
Jam is a library that provides the most popular AUTH* mechanisms right out of the box.

* [JWT](https://jam.makridenko.ru/usage/jwt/)
* [PASETO](https://jam.makridenko.ru/usage/paseto/)
* [Server side sessions](https://jam.makridenko.ru/usage/sessions/)
* [OTP](https://jam.makridenko.ru/usage/otp/)
* [OAuth2](https://jam.makridenko.ru/usage/oauth2/)

### Framework integrations

Jam provides ready-to-use integrations for the most popular frameworks:

* [FastAPI](https://jam.makridenko.ru/framework_integrations/fastapi)
* [Starlette](https://jam.makridenko.ru/framework_integrations/starlette)
* [Litestar](https://jam.makridenko.ru/framework_integrations/litestar)
* [Flask](https://jam.makridenko.ru/framework_integrations/flask)

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
