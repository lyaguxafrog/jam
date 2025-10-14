---
title: Jam instance with sessions
---

# Jam Sessions

## Instance
```python
from jam import Jam

jam = Jam(config=config)
```

## Create new session
```python
session_id: str = jam.session_create(
    session_key="some_username", data={"role": "admin"}
)
```

## Get data from session
```python
data: dict | None = jam.session_key(session_id)
```
Returns `None` if session does not exist or expired.

## Update session data
```python
jam.session_update(session_id, {"role": "user"})
```

## Delete session
```python
jam.session_delete(session_id)
```

## Clear all user sessions
```python
jam.session_clear("some_username")
```

## Rework session
```python
new_session_id: str = jam.session_rework(session_id)
```
Returns new session id and deletes old session.
