---
title: Jam instance with sessions
---

## Instance
```python
from jam import Jam

jam = Jam(config=config)
```

## Create new session
```python
session_id: str = jam.create_session(
    session_key="some_username", data={"role": "admin"}
)
```

## Get data from session
```python
data: dict | None = jam.get_session(session_id)
```
Returns `None` if session does not exist or expired.

## Update session data
```python
jam.update_session(session_id, {"role": "user"})
```

## Delete session
```python
jam.delete_session(session_id)
```

## Clear all user sessions
```python
jam.clear_sessions("some_username")
```

## Rework session
```python
new_session_id: str = jam.rework_session(session_id)
```
Returns new session id and deletes old session.


See API for more details: [Jam](../api/instance.md).