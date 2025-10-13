---
tile: How to config Jam?
---

# Jam configuration

There are several ways to configure Jam:

* yaml file
* toml file (recommended)
* python-dict

The configuration follows this pattern:
`<auth_type>: <config>`

!!! note
    This version of the config only works on jam>=2.5.1. For older versions, use the [old config](old_config.md).
    Backward compatibility is not broken, you can still use the [old config](old_config.md).

## YML/YAML Example
To configure via yml, you need to install the [`pyyaml`](https://pypi.org/project/PyYAML/) module: `pip install jamlib[yaml]`
and describe all configuration parameters in the `jam` block, for example:
```yaml
jam:
  jwt:
    alg: HS256
    secret_key: SECRET
  session:
    sessions_type: redis
    redis_uri: redis://0.0.0.0:6379/0
```

And specify the path to the file in the instance:
```python
from jam import Jam

jam = Jam(config="my_config.yml")
```

## TOML Example
To configure via toml, you need to describe all parameters in the config in the `jam` block, for example:
!!! tip
    For `python < 3.11` you need to install the [`toml`](https://pypi.org/project/toml/) module: `pip intall jamlib[toml]`
```toml
[jam.jwt]
alg = "HS256"
secret_key = "SECRET"

[jam.session]
session_type = "redis"
redis_uri = "redis://0.0.0.0:6379/0"
```

And specify the path to the file in the instance:
```python
from jam import Jam

jam = Jam(config="my_config.toml") # By default config=pyproject.toml
```

## Dict Example
To configure via dict, you need to describe all parameters in dict and pass it to the instance:
```python
from jam import Jam

config = {
    "jwt": {
        "alg": "HS256",
        "secret_key": "SECRET"
    },
    "session": {
        "sessions_type": "redis",
        "redis_uri": "redis://0.0.0.0:6379/0"
    }
}

jam = Jam(config=config)
```