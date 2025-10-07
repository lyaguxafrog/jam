---
image: assets/logo_n_title.png
---
<div style="text-align: center;">
    <img alt="logo" src="assets/loog_n_title.png" />
    <p>Welcome to Jam documentation!</p>
</div>

## About
Jam(Jeneric auth module) - This is a simple library for easy implementation
of auth* in your application!

## Installation
<!-- termynal -->
```
> pip install jamlib
---> 100%
Installed!
```
How to install dev version: -> [Jam Unstable](install_unstable.md)

## Quick start
```python
# -*- coding: utf-8 -*-

from jam import Jam

# jwt
config = {
    "auth_type": "jwt",
    "secret_key": "secret",
    "expire": 3600
}

jam = Jam(config=config)
token = jam.gen_jwt_token({"user_id": 1})  # eyJhbGciOiAiSFMyN...

# sessions
config = {
    "auth_type": "sessions",
    "session_type": "redis",
    "redis_uri": "redis://0.0.0.0:6379/0",
    "default_ttl": 30 * 24 * 60 * 60,
    "session_path": "sessions"
}

jam = Jam(config=config)
session_id = jam.create_session(
    session_key="username@somemail.com",
    data={"user_id": 1, "role": "user"}
)  # username@somemail.com:9f46...
# You alse can crypt your sessions, see: jam.makridenko.ru/sessions/session_crypt/

# OTP
# Since OTP is most often the second factor for authorization,
# in Jam, the OTP setting complements the main authorization configuration
config = {
    "auth_type": "jwt", # jwt for example
    "alg": "HS256",
    "secret_key": "SOME_SECRET",
    "otp": {
        "type": "totp",
        "digits": 6,
        "digest": "sha1",
        "interval": 30
    }
}

jam = Jam(config=config)
code = jam.get_otp_code(
    secret="USERSECRETKEY"
)  # '735891'
```

## Asynchronous support
!!! note
    You can use `jam.aio` module to work with async functions. **The methods are the same**, but you need to use `await` keyword.


```python
from jam.aio import Jam

config = {
    "auth_type": "jwt"
    "alg": "HS256",
    "secret_key": "secret",
    "expire": 2600
}
jam = Jam(config=config)
payload = await jam.make_payload(**{"user_id": 1})
token = await jam.gen_jwt_token(**payload)
```


## Why Jam?
Jam is a library that provides the most popular AUTH* mechanisms right out of the box.

* [JWT](https://jam.makridenko.ru/jwt/instance/)
* [Server side sessions](https://jam.makridenko.ru/sessions/instance/)
* OTP
    * [TOTP](https://jam.makridenko.ru/otp/totp/)
    * [HOTP](https://jam.makridenko.ru/otp/hotp/)


Why choose Jam? Jam supports many authentication methods out of the box with minimal dependencies.
Here is a comparison with other libraries:

| Features / Library    | **Jam**                                                                                               | [Authx](https://authx.yezz.me/) | [PyJWT](https://pyjwt.readthedocs.io) | [AuthLib](https://docs.authlib.org) | [OTP Auth](https://otp.authlib.org/) |
|-----------------------|-------------------------------------------------------------------------------------------------------|--------------------------------|---------------------------------------|-------------------------------------|--------------------------------------|
| JWT                   | ✅                                                                                                     | ✅ | ✅ | ✅ | ❌                                    |
| JWT black/white lists | ✅                                                                                                     | ❌ | ❌ | ❌ | ❌ |
| Server side sessions  | ✅                                                                                                     | ✅ | ❌ | ❌ | ❌                                    |
| OTP                   | ✅                                                                                                     | ❌ | ❌ | ❌ | ✅ |
| OAuth2                | ⏳                                                                                                     | ✅ | ❌ | ✅ | ❌ |
| Flexible config       | ✅                                                                                                     | ❌ | ❌ | ❌ | ❌ |
| Modularity            | ✅                                                                                                     | ❌ | ❌ | ❌ | ❌ |


## Roadmap
![ROADMAP](assets/roadmap.png)
