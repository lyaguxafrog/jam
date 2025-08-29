# Jam

![logo](https://github.com/lyaguxafrog/jam/blob/master/docs/assets/h_logo_n_title.png?raw=true)

![Static Badge](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![PyPI - Version](https://img.shields.io/pypi/v/jamlib)
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
from jam.utils import make_jwt_config

config = make_jwt_config(
    alg="HS256",
    secret_key="some-key",
    expire=36000,
)

jam = Jam(auth_type="jwt", config=config)
token = jam.gen_jwt_token({"user_id": 1})
```

## Roadmap
![Roadmap](https://jam.makridenko.ru/assets/roadmap.png?raw=true)

