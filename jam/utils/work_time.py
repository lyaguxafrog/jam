# -*- coding: utf-8 -*-

import time
from functools import wraps


def _work_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"'{func.__name__}': {execution_time:.6f}")
        return result

    return wrapper
