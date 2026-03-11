# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar


User = TypeVar("User", bound="BaseUser")


@dataclass(slots=True)
class Token:
    """Data for Authresult."""

    token: str | None


class BaseUser(ABC):
    """Abstract user model for AuthResult."""

    @abstractmethod
    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> User:
        """Build model from payload.

        Args:
            payload (dict[str, Any]): Payload for your data.
        """
        raise NotImplementedError
