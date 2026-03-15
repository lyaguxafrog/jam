---
title: JSON serialization
---

Jam makes it easy to replace the JSON serializer in your code; all you need to do is specify a serializer that inherits from `jam.BaseEncoder` in the configuration.


```python
from jam import Jam, BaseEncoder


class SomeEncoder(BaseEncoder)
    
    @classmethod
    @abstractmethod
    def dumps(cls, var: dict[str, Any]) -> bytes:
        """Dump dict."""
        # some logic

    @classmethod
    @abstractmethod
    def loads(cls, var: str | bytes) -> dict[str, Any]:
        """Load json."""
        # some logic


config = {
    "serializer": SomeEncoder,
    "jwt": {
        "alg": "HS256",
        "secret_key": "SOMESECRET"
    }
}

jam = Jam(
    config=config,
    # serializer=SomeSerializer  <- Or you can pass it as a parameter to the `jam.Jam` class
)
```


By default, Jam uses the stdlib json module for serialization. Jam also includes a pre-built serializer for [`msgspec`](https://github.com/jcrist/msgspec). To use it, you need to install [`msgspec`](https://github.com/jcrist/msgspec) and pass it to Jam:

```bash
pip install jamlib msgspec
```

```python
from jam import jam
from jam.encoders import MsgspecJsonEncoder

jam = Jam(
    config="jamconfig.yaml",
    serializer=MsgspecJsonEncoder,
)
```
