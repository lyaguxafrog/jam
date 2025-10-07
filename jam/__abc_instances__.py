# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseJam(ABC):
    """Abstract Instance object."""

    @abstractmethod
    def gen_jwt_token(self, payload) -> str:
        """Generate new JWT token."""
        raise NotImplementedError

    @abstractmethod
    def verify_jwt_token(
        self, token: str, check_exp: bool, check_list: bool
    ) -> dict[str, Any]:
        """Verify JWT token."""
        raise NotImplementedError

    @abstractmethod
    def make_payload(self, **payload) -> dict[str, Any]:
        """Generate new template."""
        raise NotImplementedError

    @abstractmethod
    def create_session(self, session_key: str, data: dict) -> str:
        """Create new session."""
        raise NotImplementedError

    @abstractmethod
    def get_session(self, session_id: str) -> Optional[dict]:
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

    @abstractmethod
    def get_otp_uri(
        self,
        secret: str,
        name: Optional[str] = None,
        issuer: Optional[str] = None,
        counter: Optional[int] = None,
    ) -> str:
        """Generates an otpauth:// URI for Google Authenticator."""
        raise NotImplementedError

    @abstractmethod
    def get_otp_code(self, secret: str, factor: Optional[int] = None) -> str:
        """Generates a OTP code."""
        raise NotImplementedError

    @abstractmethod
    def verify_otp_code(
        self,
        secret: str,
        code: str,
        factor: Optional[int] = None,
        look_ahead: Optional[int] = None,
    ) -> bool:
        """Verify TOTP code."""
        raise NotImplementedError

    @abstractmethod
    def oauth2_get_authorized_url(
        self, provider: str, scope: list[str], **extra_params: Any
    ) -> str:
        """Generate full OAuth2 authorization URL.

        Args:
            provider (str): Provider name
            scope (list[str]): Auth scope
            extra_params (Any): Extra ath params

        Returns:
            str: Authorization url
        """
        raise NotImplementedError

    @abstractmethod
    def oauth2_fetch_token(
        self,
        provider: str,
        code: str,
        grant_type: str = "authorization_code",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Exchange authorization code for access token.

        Args:
            provider (str): Provider name
            code (str): OAuth2 code
            grant_type (str): Type of oauth2 grant
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: OAuth2 token
        """
        raise NotImplementedError

    @abstractmethod
    def oauth2_refresh_token(
        self,
        provider: str,
        refresh_token: str,
        grant_type: str = "refresh_token",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Use refresh token to obtain a new access token.

        Args:
            provider (str): Provider name
            refresh_token (str): Refresh token
            grant_type (str): Grant type
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: Refresh token
        """
        raise NotImplementedError

    @abstractmethod
    def oauth2_client_credentials_flow(
        self,
        provider: str,
        scope: Optional[list[str]] = None,
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Obtain access token using client credentials flow (no user interaction).

        Args:
            provider (str): Provider name
            scope (list[str] | None): Auth scope
            extra_params (Any): Extra auth params if needed

        Returns:
            dict: JSON with access token
        """
        raise NotImplementedError
