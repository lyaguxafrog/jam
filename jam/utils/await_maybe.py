# -*- coding: utf-8 -*-

import inspect
from collections.abc import AsyncIterator, Awaitable, Iterator
from typing import TypeVar, Union


T = TypeVar("T")

AwaitableOrValue = Union[Awaitable[T], T]
AsyncIteratorOrIterator = Union[AsyncIterator[T], Iterator[T]]


async def await_maybe(value: AwaitableOrValue[T]) -> T:
    """Source: https://github.com/strawberry-graphql/strawberry/blob/main/strawberry/utils/await_maybe.py."""
    if inspect.isawaitable(value):
        return await value

    return value


__all__ = ["AsyncIteratorOrIterator", "AwaitableOrValue", "await_maybe"]
