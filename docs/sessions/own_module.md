---
title: Custom sessions backend
---

You can also create your own session module, for example,
to store sessions in PSQL or for other purposes.
To do this, you need to create your own class inheriting
from [BaseSessionModule](/api/sessions/abc_sessions_repo/).

For example:
```python
from jam.sessions import BaseSessionModule


class MyCustomSession(BaseSessionModule):
    def __init__(self, some_param: str, another_param: int) -> None:
        super().__init__()
        self.some_param = some_param
        self.another_param = another_param

    def create(self, session_key: str, data: dict) -> str:
        ...

    def get(self, session_id: str) -> dict | None:
        ...

    def update(self, session_id: str, data: dict) -> None:
        ...

    def clear(self, session_key: str) -> None:
        ...

    def rework(self, session_id: str) -> str:
        ...
```

After that, it will need to be transferred to the config with your custom parameters.

```python

from jam import Jam

config = {
    "session_type": "custom",
    "custom_module": MyCustomSession,
    "some_param": "some_value",
    "another_param": 123
}

jam = Jam(auth_type="session", config=config)
jam.create_session(session_key="some_username", data={"user_id": 1})
```