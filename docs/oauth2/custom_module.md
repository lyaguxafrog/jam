---
title: Custom module
---

If you need to extend functionality or change something,
you can write your own OAuth2 client and easily implement it in Jam.

To do this, you need to write your own class inheriting from `jam.oauth2.BaseOAuth2Client`:

```python
#app/auth/oauth2.py

from jam.oauth2 import BaseOAuth2Client


class MyCustomClient(BaseOAuth2Client):
    
    def __init__(self, some_param: str) -> None:
        ...
    
    def refresh_token(self, refresh_token: str) -> str:
        # some logic
        ...
    
    def fetch_token(self, code: str) -> str:
        # some logic
        ...
    
    def get_authorization_url(self, scope: list[str]) -> str:
        # some logic
        ...

    def client_credentials_flow(
        self, scope: Optional[list[str]] = None
    ) -> dict[str, Any]:
        # some logic
        ...
```

Now you need to enable your module in the config:
```toml
[jam]
auth_type = "oauth2"

[jam.providers.providername]
some_param = "some_value"
module = "app.auth.oauth2.MyCustomClient"
```

And use it:
```python
from jam import Jam

jam = Jam(config="config.toml")

url = jam.oauth2_get_authorized_url(
    provider="providername",
    scope=["email", "avatar"]
)
```