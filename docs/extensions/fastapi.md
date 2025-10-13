---
title: "Jam + FastAPI = <3"
---

FastAPI is fully compatible with Starlette, so use the [Starlette](starlette.md) integration.
For convenience, there is an alias in `jam.ext` imports, so you can do:
```python
from jam.ext.fastapi import JWTBackend, SessionBackend
```
Instead of:
```python
from jam.ext.starlette import JWTBackend, SessionBackend
```