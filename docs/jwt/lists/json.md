# JSONList

JSONList is a module to store tokens in json, suitable if you can't use a standalone repository like redis.

## Installing extra packages
<!-- termynal -->
```
pip install jamlib[json-lists]
---> 100%
Installed!
```

## Basic usage

### Blacklists
```python
from jam import Jam
from jam.exceptions import TokenInBlackList
from jam.jwt.lists.json import JSONList

config = {
    "alg": "HS256",
    "secret_key": "some_key",
    "expire": 3600,
    "list": JSONList(type="black", json_path="blacklist.json")
}
jam = Jam(auth_type="jwt", config=config)

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
from jam.jwt.lists.json import JSONList

config = {
    "alg": "HS256",
    "secret_key": "some_key",
    "expire": 3600,
    "list": JSONList(type="white", json_path="whitelist.json")
}
jam = Jam(auth_type="jwt", config=config)

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

jam.module.list.add(token) # Adding a token
jam.module.list.delete(token) # Deleting a token
result: bool = jam.module.list.check(token) # Check token presence in list

```