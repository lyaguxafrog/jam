# Jam

![logo](https://github.com/lyaguxafrog/jam/blob/master/docs/assets/h_logo_n_title.png?raw=true)

![Static Badge](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![PyPI - Version](https://img.shields.io/pypi/v/jamlib)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/jamlib?period=total&units=INTERNATIONAL_SYSTEM&left_color=GRAY&right_color=RED&left_text=Downloads)](https://pypi.org/project/jamlib/)
![tests](https://github.com/lyaguxafrog/jam/actions/workflows/run-tests.yml/badge.svg)
![GitHub License](https://img.shields.io/github/license/lyaguxafrog/jam)

Documentation: [jam.makridenko.ru](https://jam.makridenko.ru)

## Install
```bash
pip install jamlib
```

## Getting start
```python
# -*- coding: utf-8 -*-

from jam import Jam

config = {
    "auth_type": "jwt",
    "secret_key": "secret",
    "expire": 3600
}

jam = Jam(config=config)
token = jam.gen_jwt_token({"user_id": 1})  # eyJhbGciOiAiSFMyN...
```

## Why Jam?
| Library                               | JWT | White/Black lists for JWT | Serverside sessions | OTP | OAuth2 | Flexible config |
|---------------------------------------|-----|---------------------------|--------------------|-----|--------|-------|
| **Jam**                               | ✅   | ✅                         | ✅                  | ✅   | ⏳      | ✅     |
| [Authx](https://authx.yezz.me/)       | ✅   |  ❌                       |  ✅                  | ❌   | ✅      | ❌     |
| [PyJWT](https://pyjwt.readthedocs.io) | ✅   | ❌                         | ❌                  | ❌   | ❌      | ❌     |
| [AuthLib](https://docs.authlib.org)   | ✅   | ❌                         | ❌                  | ❌  | ✅      | ❌     |
| [OTP Auth](https://otp.authlib.org/)  | ❌   | ❌                         | ❌                  | ✅   | ❌      | ❌     |

## Roadmap
![Roadmap](https://jam.makridenko.ru/assets/roadmap.png?raw=true)

