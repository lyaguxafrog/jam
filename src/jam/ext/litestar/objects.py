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


@dataclass
class BaseUser(ABC):
    """Abstract user model for AuthResult."""

    @classmethod
    @abstractmethod
    def from_payload(cls, payload: dict[str, Any]) -> User:
        """Build model from payload.

        Args:
            payload (dict[str, Any]): Payload for your data.
        """
        raise NotImplementedError


@dataclass
class SimpleUser(BaseUser):
    """Simple user with payload."""

    payload: dict[str, Any]

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> SimpleUser:
        """Set payload=payload."""
        return cls(payload)
