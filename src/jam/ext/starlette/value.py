# -*- coding: utf-8 -*-

from typing import Any

from starlette.authentication import BaseUser


class Payload(BaseUser):
    """Auth payload."""

    def __init__(self, payload: dict[str, Any]):
        """Auth payload."""
        self.payload = payload

    @property
    def is_authenticated(self) -> bool:
        """Auth checker."""
        return True
