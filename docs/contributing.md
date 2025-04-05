# Contributing

If you want to help develop Jam, there are a few rules to follow.

## Code style
```python
# -*- coding: utf-8 -*-

# Built-in libraries
from typing import Literal

# Third-party libraries
from Crypto import Hash

# Library modules
from jam.jwt.__utils__ import __base64url_decode__


class SomeClass:
    """Long class description."""
    
    def __init__(self, some_value: str) -> None:
        """Class constructor.
        
        Args:
            some_value (str): Some value
        """
        self.sv = some_value

    def some_method(self, something: int) -> int:
        """Method Description.
        
        Args:
            something (int): Argument description
        
        Raises:
            ValueError: if something < 1
            
        Returns:
            (int)
        """
        if something < 1:
            raise ValueError("something < 1")

        return something + 1
```
Line length 80 characters, indented 4 spaces.

## Gitflow

### Commits:

The project must have `pre-commit`

* `[+]` Adding new functionality.
* `[-]` Removing something, e.g. removing a function or deleting a file.
* `[*]` Changing the logic.
* `[~]` Changes that do not affect the logic, documentation, linters, etc.

The keys in the commit body are also used:
* `R`(reason): Reason for change, deletion, etc
* `FB`(fix by): How it was made or fixed
* `N`(note): A note of some kind

Example of a correct commit
```
[*] Changed JWT decryption logic
R: Used a third-party heavy dependency that slowed down the code
FB: Removed the dependency and wrote independently 
```

### Branches
The project has two main branches:
* `stable` - Stable code of the latest release
* `develop` - Code ready for release at any moment

All branches are created from `develop` and adhere to strict branch naming:

* New feature: `feature/<id-issue-if-it-is>-<pair-words-about-feature>`
* Bug fixes: `fix/<id-issue-if-it-is>-<pair-words-about-bug>`
* Refactoring: `refactor/<id-issue-if-it-is>-<what-exactly-you-do>`
* Writing documentation: `docs/<what-exactly-you-do>`.

Examples:

* `feature/validate-redis-session`
* `fix/18-jwt-making`

### Pull requests

The title of the pull request must contain a keyword:
* `FEAT` Adding a new feature
* `BUGFIX` Bug fix
* `HOTFIX` Urgent bug fix
* `DOCS` Edits/additions to documentation

There is a template for the poolquest, 
in it clearly describe what you did and why.

Example:
```markdown
<!--this is a title -->
FEAT Validation of a redis session

## What was done
* <!--A brief description of what we've done-->
*

## Test report
<!-- Describe how you tested -->
```
