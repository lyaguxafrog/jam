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

## YAML Configuration

To configure via YAML, you need to install the [`pyyaml`](https://pypi.org/project/PyYAML/) module: `pip install jamlib[yaml]`

All configuration parameters must be described in the `jam` block:

```yaml
jam:
  jwt:
    alg: HS256
    secret_key: SECRET
  session:
    sessions_type: redis
    redis_uri: redis://0.0.0.0:6379/0
```

Specify the path to the file in the instance:
```python
from jam import Jam

jam = Jam(config="my_config.yml")
```

## TOML Configuration

To configure via TOML, describe all parameters in the config in the `jam` block:

!!! tip
    For `python < 3.11` you need to install the [`toml`](https://pypi.org/project/toml/) module: `pip install jamlib[toml]`

```toml
[jam.jwt]
alg = "HS256"
secret_key = "SECRET"

[jam.session]
session_type = "redis"
redis_uri = "redis://0.0.0.0:6379/0"
```

Specify the path to the file in the instance:
```python
from jam import Jam

jam = Jam(config="my_config.toml")  # By default config=pyproject.toml
```

## Dict Configuration

You can also pass configuration as a Python dictionary:

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

## Environment Variables

Both YAML and TOML configuration formats support environment variable substitution.

### Syntax

Jam supports three formats for environment variables:

| Format | Description | Example |
|--------|-------------|---------|
| `${VAR}` | Required variable - raises error if not set | `${JWT_SECRET}` |
| `${VAR:-default}` | Variable with default value | `${JWT_ALG:-HS256}` |
| `$VAR` | Short form - raises error if not set | `$JWT_SECRET` |

### Example with Environment Variables

**YAML:**
```yaml
jam:
  jwt:
    alg: ${JWT_ALGORITHM:-HS256}  # Default to HS256 if not set
    secret_key: ${JWT_SECRET}     # Required, will fail if not set
  session:
    sessions_type: redis
    redis_uri: redis://${REDIS_HOST:-localhost}:${REDIS_PORT:-6379}/0
  oauth2:
    providers:
      google:
        client_id: ${GOOGLE_CLIENT_ID}
        client_secret: ${GOOGLE_CLIENT_SECRET}
```

**TOML:**
```toml
[jam.jwt]
alg = "${JWT_ALGORITHM:-HS256}"
secret_key = "${JWT_SECRET}"

[jam.session]
session_type = "redis"
redis_uri = "redis://${REDIS_HOST:-localhost}:${REDIS_PORT:-6379}/0"

[jam.oauth2.providers.google]
client_id = "${GOOGLE_CLIENT_ID}"
client_secret = "${GOOGLE_CLIENT_SECRET}"
```

## Main Jam configuration

* `logger`: `str` = `jam.logger.JamLogger`

Path to logger module.

* `log_level`: `str` = `INFO`

Log level.


* `serializer`: `str` = `jam.encoders.JsonEncoder`

Path to json encoder/decoder. 


## Example

### TOML
```toml
[jam]
log_level = "DEBUG"
serializer = "jam.encoders.MsgspecJsonEncoder"

[jam.jwt]
alg = "HS256"
secret = $JWT_SECRET
```

### YAML

```yaml
jam:
  logger: myapp.customlogger.SomeCustomLogger
  log_level: INFO
  jwt:
    alg: HS512
    expire: 1200
```