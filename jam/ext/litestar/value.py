# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class User:
    """User model."""

    payload: dict[str, Any]


@dataclass
class Auth:
    """Auth model."""

    token: str


@dataclass
class AuthMiddlewareSettings:
    """Setting for jam middleware."""

    cookie_name: Optional[str]
    header_name: Optional[str]
    user_dataclass: Any
    auth_dataclass: Any
