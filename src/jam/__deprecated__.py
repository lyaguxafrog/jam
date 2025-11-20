# -*- coding: utf-8 -*-

import functools
from typing import Optional
import warnings


def deprecated(replacement: Optional[str] = None):
    """Mark funcs are deprecated."""

    def decorator(func):
        msg = f"Function {func.__name__}() is deprecated."
        if replacement:
            msg += f" {replacement}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        wrapper.__deprecated__ = True
        wrapper.__doc__ = (
            func.__doc__ or ""
        ) + f"\n\n⚠️ Deprecated: {replacement or ''}".strip()
        return wrapper

    return decorator
