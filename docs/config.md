---
title: How to config Jam?
---

# Jam configuration

There are several ways to configure Jam:

* yaml file
* toml file (recommended)
* python-dict

## YML/YAML
To configure via yml, you need to install the [`pyyaml`](https://pypi.org/project/PyYAML/) module: `pip install jamlib[yaml]`
and describe all configuration parameters in the `jam` block, for example:

```yml
jam:
  auth_type: "jwt"
  alg: HS256
  secret_key: my_secret
  expire: 3600
```

And specify the path to the file in the instance:
```python
from jam import Jam

jam = Jam(config="my_config.yml")
```

## TOML
To configure via toml, you need to describe all parameters in the config in the `jam` block, for example:
!!! tip
    For `python < 3.11` you need to install the [`toml`](https://pypi.org/project/toml/) module: `pip intall jamlib[toml]`
```toml
[jam]
auth_type = "jwt"
alg = "HS256"
secret_key = "my_secret"
expire = 3600
```

And specify the path to the file in the instance:
```python
from jam import Jam

jam = Jam(config="my_config.toml") # By default config=pyproject.toml
```

## Dict
To configure via dict, you need to describe all parameters in dict and pass it to the instance:
```python
from jam import Jam

config = {
    "auth_type": "jwt",
    "alg": "HS256",
    "secret_key": "my_secret",
    "expire": 3600
}

jam = Jam(config=config)
```