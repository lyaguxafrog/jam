
# Jam

![Static Badge](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![tests](https://github.com/lyaguxafrog/jam/actions/workflows/run-tests.yml/badge.svg) ![License](https://img.shields.io/badge/Licese-MIT-grey?link=https%3A%2F%2Fgithub.com%2Flyaguxafrog%2Fjam%2Fblob%2Frelease%2FLICENSE.md)

Simple and univirsal library for authorization. 

## Install
```bash
pip install jamlib
```

## Example

```python
from jam import JAMConfig, Jam

config: JAMConfig = JAMConfig(
    JWT_ACCESS_SECRET_KEY="some_secret_key",
    JWT_REFRESH_SECRET_KEY="another_secret_key",
)

jam: Jam = Jam(config=config)


access_key: str = jam.gen_tokens.get("access_key")
```
