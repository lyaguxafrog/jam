---
title: Custom sessions backend
---

You can also create your own session module, for example,
to store sessions in PSQL or for other purposes.
To do this, you need to create your own class inheriting
from [BaseSessionModule](/api/sessions/base_session_module/).

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

```toml
[jam]
auth_type = "session"
session_type = "custom"
custom_module = "myapp.custom_session.MyCustomSession"
# your params
some_param = "value"
another_param = 123
```