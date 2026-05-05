## Code style
Line length: 80 characters
Docstrings: Google-style with type specifications, example:
```python
# -*- coding: utf-8 -*-

import os  # stdlib

import cryptography  # libs

from jam.some.__base__ import BaseSomeClass  # our modules


def some_func(
    self,
    some_param: int,
    another_param: srt | None = None
) -> bool:
    """Function description
    
    Args:
        some_param (int): Parameter description
        another_param (str | None): Parameter description
    
    Raises:
        ValueError: Error cause description
    
    Returns:
        bool: Response description
    """
    ...

class SomeClass(BaseSomeClass):
    """A long and detailed description of the class."""

    def some_class_func(
        self,
        arg_one: int,
        arg_two: bool = False
    ) -> None:
        """Class method description.

        Args:
            arg_one (int): Some arg
            arg_two (bool): Another arg

        Returns:
            None
        """
        ...
```

## Recommended flow
```
Writing an interface
    |
    |
    V
Writing tests for it
    |
    |
    V
Implementation
    |
    |
    V
Documentation
```

The interfaces of each class are named `Base + Interface Name` and are described in `__base__.py`.
