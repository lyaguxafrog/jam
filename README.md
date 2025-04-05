# Jam

![logo](https://github.com/lyaguxafrog/jam/blob/stable/docs/assets/h_logo_n_title.png?raw=true)

![Static Badge](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![tests](https://github.com/lyaguxafrog/jam/actions/workflows/run-tests.yml/badge.svg)
![License](https://img.shields.io/badge/Licese-MIT-grey?link=https%3A%2F%2Fgithub.com%2Flyaguxafrog%2Fjam%2Fblob%2Frelease%2FLICENSE.md)

## Install
```bash
pip install jamlib
```

## Getting start
```python
# -*- coding: utf-8 -*-

from typing import Any

from jam import Jam

config: dict[str, Any] = {
        "jwt_secret_key": "some-secret",
        "expire": 3600
    }

data = {
    "user_id": 1,
    "role": "admin"
}

jam = Jam(auth_type="jwt", config=config)

payload = jam.make_payload(**data)
token = jam.gen_jwt_token(**payload)
```

## Roadmap
![Roadmap](https://github.com/lyaguxafrog/jam/blob/stable/docs/assets/roadmap.png?raw=true)

&copy; [Adrian Makridenko](https://github.com/lyaguxafrog) 2025
