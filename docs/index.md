---
title: Home
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

## Asynchronous support
!!! note
    You can use `jam.aio` module to work with async functions. **The methods are the same**, but you need to use `await` keyword.


```python
from jam.aio import Jam

config = {
    "auth_type": "jwt",
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

* [JWT](jwt/instance.md)
* [Server side sessions](instance.md)
* OTP
    * [TOTP](otp/totp.md)
    * [HOTP](otp/hotp.md)
* [OAuth2](oauth2/instance.md)


Why choose Jam? Jam supports many authentication methods out of the box with minimal dependencies.
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


## Roadmap
![ROADMAP](assets/roadmap.png)
