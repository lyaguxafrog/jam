# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseJam(ABC):
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
    def create_session(self, session_key: str, data: dict) -> Any:
        """Create new session."""
        raise NotImplementedError

    @abstractmethod
    def get_session(self, session_id: str) -> Any:
        """Retrieve session data by session ID."""
        raise NotImplementedError

    @abstractmethod
    def delete_session(self, session_id: str) -> Any:
        """Delete a session by its ID."""
        raise NotImplementedError

    @abstractmethod
    def update_session(self, session_id: str, data: dict) -> Any:
        """Update session data by session ID."""
        raise NotImplementedError

    @abstractmethod
    def clear_sessions(self, session_key: str) -> Any:
        """Clear all sessions associated with a specific session key."""
        raise NotImplementedError

    @abstractmethod
    def rework_session(self, old_session_key: str) -> Any:
        """Rework an existing session key to a new one."""
        raise NotImplementedError

    @abstractmethod
    def get_otp_uri(
        self,
        secret: str,
        name: Optional[str] = None,
        issuer: Optional[str] = None,
        counter: Optional[int] = None,
    ) -> Any:
        """Generates an otpauth:// URI for Google Authenticator."""
        raise NotImplementedError

    @abstractmethod
    def get_otp_code(self, secret: str, factor: Optional[int] = None) -> Any:
        """Generates a OTP code."""
        raise NotImplementedError

    @abstractmethod
    def verify_otp_code(
        self,
        secret: str,
        code: str,
        factor: Optional[int] = None,
        look_ahead: Optional[int] = None,
    ) -> Any:
        """Verify TOTP code."""
        raise NotImplementedError
