---
title: How to config Jam?
---

# Jam configuration

There are several ways to configure Jam:
* yaml file
* toml file (recommended)
* python-dict

## YML/YAML
To configure via yml, you need to describe all configuration parameters in the `jam` block, for example:

```yml
jam:
  alg: HS256
  secret_key: my_secret
  expire: 3600
```

And specify the path to the file in the instance:
```python
from jam import Jam

jam = Jam(auth_type="jwt", config="my_config.yml")
```

## TOML
To configure via toml, you need to describe all parameters in the config in the `jam.config` block, for example:
```toml
[jam.config]
alg = "HS256"
secret_key = "my_secret"
expire = 3600
```

And specify the path to the file in the instance:
```python
from jam import Jam

jam = Jam(auth_type="jwt", config="my_config.toml") # By default config=pyproject.toml
```

## Dict
To configure via dict, you need to describe all parameters in dict and pass it to the instance:
```python
from jam import Jam

config = {
    "alg": "HS256",
    "secret_key": "my_secret",
    "expire": 3600
}

jam = Jam(auth_type="jwt", config=config)
```