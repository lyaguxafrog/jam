---
title: Password utils
---

Since Jam is a library for auth*, it would be nice to secure your passwords, wouldn't it?

Jam has utilities for generating a password hash with salt
## Generate password hash
```python
from jam.utils import hash_password

my_password = "qwerty1234"

salt, hash_ = hash_password(
    password=my_password
)
print(salt)  # 865e3c3ae40a822ace7400c1e20aa9f7
print(hash_)  # d11a48d3613df679445cdf9a3068e2f5e80b382ea9a5b908a7336d3f989231a9
```
To make it convenient to store this hash in a database(for example), you can serialize the hash:

```python
from jam.utils import serialize_hash

serialized_hash = serialize_hash(
    salt_hex=salt, hash_hex=hash_
)  # 865e3c3ae40a822ace7400c1e20aa9f7$d11a48d3613df679445cdf9a3068e2f5e80b382ea9a5b908a7336d3f989231a9
```

## Check passwords
Now, when a user, for example, wants to log into his account, and we need
to verify his password, we use utilities to verify the password with a hash:

First you need to deserialize the hash
```python
from jam.utils import deserialize_hash

serialized_hash = "865e3c3ae40a822ace7400c1e20aa9f7$d11a48d3613df679445cdf9a3068e2f5e80b382ea9a5b908a7336d3f989231a9"
salt, hash_ = deserialize_hash(serialized_hash)
```

And now we can compare passwords.
```python
from jam.utils import check_password

input_while_login_password = "qwerty1234"


result: bool = check_password(
    password=input_while_login_password,
    salt_hex=salt,
    hash_hex=hash_
)  # True
```