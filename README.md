# Jam

![logo](https://github.com/lyaguxafrog/jam/blob/master/docs/assets/h_logo_n_title.png?raw=true)

![Static Badge](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
[![PyPI - Version](https://img.shields.io/pypi/v/jamlib)](https://pypi.org/project/jamlib/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/jamlib?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=RED&left_text=Downloads)](https://pypi.org/project/jamlib/)
![tests](https://github.com/lyaguxafrog/jam/actions/workflows/run-tests.yml/badge.svg)
[![GitHub License](https://img.shields.io/github/license/lyaguxafrog/jam)](https://github.com/lyaguxafrog/jam/blob/master/LICENSE.md)

Documentation: [jam.makridenko.ru](https://jam.makridenko.ru)


## Install
```bash
pip install jamlib
```

## Why Jam?
Jam is a library that provides the most popular AUTH* mechanisms right out of the box.

* [JWT](https://jam.makridenko.ru/jwt/instance/)
* [Server side sessions](https://jam.makridenko.ru/sessions/instance/)
* OTP
  * [TOTP](https://jam.makridenko.ru/otp/totp/)
  * [HOTP](https://jam.makridenko.ru/otp/hotp/)
* [OAuth2](https://jam.makridenko.ru/oauth2/instance/)

### Framework integrations

Jam provides ready-to-use integrations for the most popular frameworks:

* [FastAPI](https://jam.makridenko.ru/extensions/fastapi)
* [Starlette](https://jam.makridenko.ru/extensions/starlette)
* [Litestar](https://jam.makridenko.ru/extensions/litestar)
* [Flask](https://jam.makridenko.ru/extensions/flask)

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

