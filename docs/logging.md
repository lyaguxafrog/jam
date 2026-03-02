---
title: Logging
---

By default, Jam uses `JamLogger`, a class that utilizes standard `logging`.
Therefore, you can use the standard Python method to collect logs:

```python
import logging

logger = logging.getLogger("jam")
```

If for some reason you are not satisfied with the standard logger,
you can easily replace it in `Jam` using `BaseLogger`:
```python
from jam import Jam, BaseLogger

class YourCustomLogger(BaseLogger):
    
    def __init__(self, log_level: str):
        ...
    
    def info(self, message: str):
        # your logger implementation here
        pass
        
    def warning(self, message: str):
        # your logger implementation here
        pass
        
    def error(self, message: str):
        # your logger implementation here
        pass
        
    def critical(self, message: str):
        # your logger implementation here
        pass


jam = Jam(logger=BaseLogger)    
```
