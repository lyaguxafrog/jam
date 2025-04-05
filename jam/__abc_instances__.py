# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any


class __AbstractInstance(ABC):
    """Abstract Instance object."""

    @abstractmethod
    def gen_jwt_token(self, payload) -> str:
        """Generate new JWT token."""
        raise NotImplementedError

    @abstractmethod
    def verify_jwt_token(
        self, token: str, check_exp: bool, check_list: bool
    ) -> Any:
        """Verify JWT token."""
        raise NotImplementedError

    @abstractmethod
    def make_payload(self, **payload) -> Any:
        """Generate new template."""
        raise NotImplementedError
