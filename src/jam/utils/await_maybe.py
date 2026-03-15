# -*- coding: utf-8 -*-

from collections.abc import Awaitable
import inspect
from typing import TypeVar


T = TypeVar("T")

AwaitableOrValue = Awaitable[T] | T
AsyncIteratorOrIterator = Awaitable[T] | T


async def await_maybe(value: AwaitableOrValue[T]) -> T:
    """Source: https://github.com/strawberry-graphql/strawberry/blob/main/strawberry/utils/await_maybe.py."""
    if inspect.isawaitable(value):
        return await value

    return value


__all__ = ["AsyncIteratorOrIterator", "AwaitableOrValue", "await_maybe"]
