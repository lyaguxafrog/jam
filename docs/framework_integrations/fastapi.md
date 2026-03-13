---
title: FastAPI
---

FastAPI is fully compatible with Starlette, so use the [Starlette integration](/framework_integrations/starlette). For convenience, there is an alias in `jam.ext` imports, so you can do:

```python
from jam.ext.fastapi import JWTBackend, SessionBackend, PASETOBackend
```

Instead of:

```python
from jam.ext.starlette import JWTBackend, SessionBackend, PASETOBackend
```
