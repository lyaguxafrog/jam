# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any


class __AbstractInstance(ABC):
    """Abstract Instance object."""

    @abstractmethod
    def gen_jwt_token(self, payload) -> Any:
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

    @abstractmethod
    def create_session(self, session_key: str, data: dict) -> str:
        """Create new session."""
        raise NotImplementedError

    @abstractmethod
    def get_session(self, session_id: str) -> dict | None:
        """Retrieve session data by session ID."""
        raise NotImplementedError

    @abstractmethod
    def delete_session(self, session_id: str) -> None:
        """Delete a session by its ID."""
        raise NotImplementedError

    @abstractmethod
    def update_session(self, session_id: str, data: dict) -> None:
        """Update session data by session ID."""
        raise NotImplementedError

    @abstractmethod
    def clear_sessions(self, session_key: str) -> None:
        """Clear all sessions associated with a specific session key."""
        raise NotImplementedError

    @abstractmethod
    def rework_session(self, old_session_key: str) -> str:
        """Rework an existing session key to a new one."""
        raise NotImplementedError
