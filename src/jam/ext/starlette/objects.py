# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from starlette.authentication import BaseUser as StarletteBaseUser


class BaseUser(ABC, StarletteBaseUser):
    """BaseUser with builder from payload."""

    @classmethod
    @abstractmethod
    def from_payload(cls, payload: dict[str, Any]) -> BaseUser:
        """Create instance by payload.

        Args:
            payload (dict[str, Any]): Payload from auth

        Example:
        ```python

        class MyUser(JamBaseUser):
            id: int
            username: str

            @classmethod
            def from_payload(cls, payload):
                return cls(
                    id=payload["id"],
                    username=payload["username"]
                )

        payload = jwt.decode(token)
        user = MyUser.from_payload(payload)
        ```
        """
        raise NotImplementedError


@dataclass(slots=True)
class SimpleUser(BaseUser):
    """Simple user with payload only."""

    payload: dict[str, Any]

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> SimpleUser:  # noqa
        return cls(payload=payload)

    def is_authenticated(self) -> bool:  # type: ignore # noqa
        return True
