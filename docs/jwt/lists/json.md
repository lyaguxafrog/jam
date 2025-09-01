# JSONList

JSONList is a module to store tokens in json, suitable if you can't use a standalone repository like redis.

## Installing extra packages
<!-- termynal -->
```
pip install jamlib[json]
---> 100%
Installed!
```

## Basic usage

### Configuration

### `type`: `str`
List type, black or white.

### `backend`: `str`
Which backend to use for storing the list.

### `json_path`: `str`
Path to json file.

Example `toml` config:
```toml
[jam]
auth_type = "jwt"
secret_key = "SECRET"
expire = 3600

[jam.list]
type="white" # or black
backend="json"
json_path="my_whitelist.json"
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
jam.module.list.delete(new_token)
```

## Other methods
```python

# All methods are valid for both black and white lists

token: str = "some_token"

jam.list.add(token) # Adding a token
jam.list.delete(token) # Deleting a token
result: bool = jam.list.check(token) # Check token presence in list
```