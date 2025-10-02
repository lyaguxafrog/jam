---
title: Key generators
---

Jam has several utilities for generating various keys.

## AES Keys
For convenient generation of AES keys, there is a utility `jam.utils.aes.generate_aes_key`:
```python
from jam.utils import generate_aes_key

key: bytes = generate_aes_key()
```
Now this key can be used in [AES session encryption](/sessions/session_crypt/) or somewhere else in your application.

## RSA Keys
To generate an RSA key pair, you can use `jam.utils.rsa.generate_rsa_key_pair`

```python
from jam.utils import generate_rsa_key_pair

keys: dict[str, str] = generate_rsa_key_pair(
    key_size=2048
) # you get a dictionary like `{"private": KEY, "public": KEY}
```

## OTP Keys
OTPs have a specific key format, so jam also has a utility for simple key generation.

```python
from jam.utils import generate_otp_key

key = generate_otp_key(entropy_bits=128) # RQTC2QCAFRVB6DETJCZ2CST4PI
```