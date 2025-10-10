# -*- coding: utf-8 -*-

import functools
import warnings


def __deprecated__(reason: str = ""):
    """Decorator for deprecated methods.

    Args:
        reason (str): Reason
    """

    def decorator(func):
        message = f"Call to deprecated function {func.__name__}()."
        if reason:
            message += f" {reason}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)
            warnings.warn(message, category=DeprecationWarning, stacklevel=2)
            warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)

        if func.__doc__:
            wrapper.__doc__ = (
                func.__doc__.rstrip()
                + f"\n\nDeprecated:\n    {reason or 'This function is deprecated.'}"
            )
        else:
            wrapper.__doc__ = (
                f"Deprecated:\n    {reason or 'This function is deprecated.'}"
            )

        wrapper.__deprecated__ = True
        return wrapper

    return decorator
