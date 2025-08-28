---
title: AES Encryption in Jam
---

You can use [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) encryption to generate a session.

To do this, pass the `is_session_crypt` and `session_aes_secret` parameters with the encryption key to `config`.
The encryption key can be generated using the `jam.utils.generate_aes_key()` function.

```python
from jam import Jam
from jam.utils import generate_aes_key

aes_key = generate_aes_key()
config = {
    "session_type": "redis",
    "is_session_crypt": True,
    "session_aes_secret": aes_key,
    "redis_uri": "redis://localhost:6379/0",
    "session_path": "sessions",
    "default_ttl": 3600,
}

jam = Jam(auth_type="session", config=config)
```

Now, when generating a session, the session ID will be encrypted using AES:
```python
session_id: str = jam.create_session(
    session_key="some_username",
    data={"role": "admin"}
)
print(session_id)  # J$_gAAAAABosJAjGhsz_qZScNCZwvQVTgIs45wxvSNmkKUHkOcZG5vTW97wBxnRdO3-3zQWICwYJ6qGCxvZO8uEigLHuLIWpUDYef-FTrgqGNjbx1jAY8wdMqIusLLZR4I8A8VW6r0ugrqB
```
