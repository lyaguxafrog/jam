# jam

![Static Badge](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![tests](https://github.com/lyaguxafrog/jam/actions/workflows/run-tests.yml/badge.svg) ![License](https://img.shields.io/badge/Licese-MIT-grey?link=https%3A%2F%2Fgithub.com%2Flyaguxafrog%2Fjam%2Fblob%2Frelease%2FLICENSE.md)


> [!CAUTION]
> In active development! Cannot be used in real projects!
> 


## Features
- [x] JWT Making
- [ ] Another crypt alghorutms
- [ ] White/Black lists
- [ ] Session Maker
- [ ] Integration with Django, FastAPI, Strawberry
- [ ] OAuth2


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


tokens = jam.jwt_gen_tokens()
access_token: str = tokens.access
print(access_token)
# 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJkYXRhIjoge30sICJleHAiOiAxNzM3NzI5MDI3fQ.07gECSzAqetFYgToOFvBTSYjEAzWlZYmzucDL7Lgeno'
```
