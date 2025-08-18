---
image: assets/logo_n_title.png
---

# Jam

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

## Quick start
```python
from jam import Jam

# you can use jam.utils.make_jwt_config to generate the config easily
config = {
    "alg": "HS256",
    "secret_key": "secret",
    "expire": 2600
}

jam = Jam(auth_type="jwt", config=config)
payload = jam.make_payload(**{"user_id": 1})
token = jam.gen_jwt_token(**payload)
```

## Asynchronous support
!!! note
    You can use `jam.aio` module to work with async functions. **The methods are the same**, but you need to use `await` keyword.


```python
from jam.aio import Jam

config = {
    "alg": "HS256",
    "secret_key": "secret",
    "expire": 2600
}
jam = Jam(auth_type="jwt", config=config)
payload = await jam.make_payload(**{"user_id": 1})
token = await jam.gen_jwt_token(**payload)
```

## Roadmap
![ROADMAP](assets/roadmap.png)
