# RedisList

RedisList is a module for storing tokens in redis, great because you can put the lifetime of a token in the list.

You need a running redis instance for this to work.

## Installing extra packages
<!-- termynal -->
```
pip install jamlib[redis]
---> 100%
Installed!
```

## Basic usage

## Configuration

### `type`: `str`
List type, black or white.

### `backend`: `str`
Which backend to use for storing the list.

### `redis_uri`: `str`
URI to redis connection.

### `in_list_life_time`: `int`
Token lifetime in seconds.

Example `toml` config:
```toml
[jam]
auth_type = "jwt"
expire = 3600
secret_key = "SECRET_KEY"

[jam.list]
type = "white" # or black
backend = "redis"
redis_uri = "redis://0.0.0.0:6379/0"
in_list_life_time = 3600
```

### Blacklists
```python
from jam import Jam
from jam.exceptions import TokenInBlackList

jam = Jam(config="config.toml")

some_token = "eyJhbGc0..."

try:
    payload = jam.verify_jwt_token(token=some_token, check_list=True)
# If the token is in the blacklist
# during the validation, jam will return an error
except TokenInBlackList:
    print("Token in black list!")

# To add a token to the blacklist
jam.module.list.add(some_token)
```

### Whitelists
```python
from jam import Jam
from jam.exceptions import TokenNotInWhiteList

jam = Jam(config="config.toml")

# As soon as you create a new token, it goes on the whitelist
new_token = jam.gen_jwt_token({"user_id": 1})

try:
    jam.verify_jwt_token(token=new_token, check_list=True)

# If the token is not found in the whitelist, jam will return an error
except TokenNotInWhiteList:
    print("Token not in whitelist!")

# To remove a token from the whitelist
jam.list.delete(new_token)
```

## Other methods
```python

# All methods are valid for both black and white lists

token: str = "some_token"

jam.list.add(token) # Adding a token
jam.list.delete(token) # Deleting a token
result: bool = jam.list.check(token) # Check token presence in list
```