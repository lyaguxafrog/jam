# Jam

![Static Badge](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![tests](https://github.com/lyaguxafrog/jam/actions/workflows/run-tests.yml/badge.svg) ![License](https://img.shields.io/badge/Licese-MIT-grey?link=https%3A%2F%2Fgithub.com%2Flyaguxafrog%2Fjam%2Fblob%2Frelease%2FLICENSE.md)
![jam](https://img.shields.io/badge/jam-3.1.0_alpha-white?style=flat&labelColor=red)


> [!CAUTION]
> In active development! Cannot be used in real projects!
> 

## Install
```bash
pip install jamlib
```
or from repo:
```bash
git clone https://github.com/lyaguxafrog/jam.git && \
cd jam/ && uv sync --no-dev  # need to install uv
```

## Getting start
```python
# -*- coding: utf-8 -*-

from typing import Any

from jam import Jam
from jam.utils import make_jwt_config

config = make_jwt_config(
            alg="HS256",
            secret_key="some_secret",
            expire=18000
    )

data = {
    "user_id": 1,
    "role": "admin"
}

jam = Jam(auth_type="jwt", config=config)

payload = jam.make_payload(**data)
token = jam.gen_jwt_token(**payload)
```

## Roadmap
![Roadmap](assets/roadmap.png)
