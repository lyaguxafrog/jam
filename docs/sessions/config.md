---
title: Jam sessions configuration
---

# Config

Config is a dict that stores session settings.

```python
config = {
    "session_type": "redis",
    "is_session_crypt": False,
    # Settings for a specific module here
    "redis_uri": "redis://localhost:6379/0",
    "session_path": "sessions",
    "default_ttl": 3600,
}
```

## General parameters

### `session_type`

Session type. Available options are `redis`, `json`, `custom`.
For `custom`, you will need to specify your session class in the `custom_module` parameter.

### `is_session_crypt`
Sometimes you need to encrypt the session ID so that it cannot be forged.
If you want to encrypt the session ID, set this parameter to `True` and pass the encryption key in the `session_aes_secret` parameter.

### `session_aes_secret`
The encryption key for the session ID. Key must be 32 url-safe base64-encoded bytes. 
You can use [`jam.utils.generate_aes_key`](/api/utils/aes/) to generate it.

### `id_factory`
The function for generating the session ID. The default is `uuid.uuid4()`.

## Redis

In Redis, sessions are stored as `HASH`, where `name` is constructed from `<session_path>:<session_key>`.
The session ID is used as the `key`, and a serialized JSON object with session data is used as the `value`.

### `redis_uri`
URI for connecting to Redis.

### `default_ttl`
Session lifetime in seconds. The default is 3600 (1 hour). If `None`, the session will not be deleted.

### `session_path`
Prefix for session keys in Redis. The default is `sessions`.

More details: [jam.sessions.redis.RedisSessions](/api/sessions/redis/)

## JSON

In JSON, sessions are stored as files in the directory specified in the `json_path` parameter.

### `json_path`
The path to the directory where session files will be stored.

More details: [jam.sessions.json.JsonSessions](/api/sessions/tinydb/)

## Custom

### `custom_module`
Your custom session module. It must be a subclass of [`BaseSessionModule`](/api/sessions/abc_sessions_repo/).

### Other parameters

For a custom module, simply specify the parameters you need in dict, for example:
```python
from jam.sessions import BaseSessionModule

class MySession(BaseSessionModule):
    ...

config = {
    "session_type": "custom",
    "custom_module": MySession,
    "my_param1": "value1",
    "my_param2": "value2",
}
```

See more: [Own sessions backend](/sessions/own_module/)