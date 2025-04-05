# Custom Module

If you want to store tokens somewhere else, for example,
or validate in some other way, you can easily write your own module.

```python
from typing import Literal
from jam.jwt.lists import ABCList

class MyCustomList(ABCList):
    def __init__(self, type: Literal["white", "black"], some_arg: str) -> None:
        super().__init__(list_type=type)
        self.my_arg = some_arg

    def add(self, token: str) -> None:
        # some logic for adding a token to the list
        pass
    
    def check(self, token: str) -> bool:
        # some logic to check if the token is in the list
        pass
    
    def delete(self, token: str) -> None:
        # some logic for removing a token from the list
        pass

config = {
    "alg": "HS256",
    "secret_key": "some_key",
    "expire": 3600,
    "list": MyCustomList(type="black", some_arg="some_value")
}
```
And now you can use it as a `JSONList` or `RedisList`.