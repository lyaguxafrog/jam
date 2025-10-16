# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from jam.__logger__ import logger
from jam.utils.config_maker import __module_loader__


class BaseJam(ABC):
    """Abstract Instance object."""

    _JAM_MODULES: dict[str, str] = {}

    def build_module(self, name: str, cfg: dict[str, Any]):
        """Method for building module from config.

        Args:
            name (str): Module name
            cfg (dict[str, Any]): Config
        """
        module_path = cfg.pop("module", None)
        if not module_path:
            module_path = self._JAM_MODULES.get(name)

        if not module_path:
            raise NotImplementedError(f"Auth module '{name}' is not supported")

        logger.debug(f"Initializing module '{name}' from {module_path}")
        module_cls = __module_loader__(module_path)

        # FIX: handle oauth2 specially
        if name == "oauth2":
            return module_cls(config=cfg)

        return module_cls(**cfg)

    @abstractmethod
    def jwt_make_payload(
        self, exp: Optional[int], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Make JWT-specific payload.

        Args:
            exp (int | None): Token expire, if None -> use default
            data (dict[str, Any]): Data to payload

        Returns:
            dict[str, Any]: Payload
        """
        raise NotImplementedError

    @abstractmethod
    def jwt_create_token(self, payload: dict[str, Any]) -> str:
        """Create JWT token.

        Args:
            payload (dict[str, Any]): Data payload

        Returns:
            str: New token

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        """
        raise NotImplementedError

    @abstractmethod
    def jwt_verify_token(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Any]:
        """Verify and decode JWT token.

        Args:
            token (str): JWT token
            check_exp (bool): Check expire
            check_list (bool): Check white/black list. Docs: https://jam.makridenko.ru/jwt/lists/what/

        Returns:
            dict[str, Any]: Decoded payload

        Raises:
            ValueError: If the token is invalid.
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None.
            EmtpyPublicKey: If RSA algorithm is selected, but public key None.
            NotFoundSomeInPayload: If 'exp' not found in payload.
            TokenLifeTimeExpired: If token has expired.
            TokenNotInWhiteList: If the list type is white, but the token is  not there
            TokenInBlackList: If the list type is black and the token is there
        """
        raise NotImplementedError

    @abstractmethod
    def session_create(self, session_key: str, data: dict[str, Any]) -> str:
        """Create new session.

        Args:
            session_key (str): Key for session
            data (dict[str, Any]): Session data

        Returns:
            str: New session ID
        """
        raise NotImplementedError

    @abstractmethod
    def session_get(self, session_id: str) -> Optional[dict[str, Any]]:
        """Get data from session.

        Args:
            session_id (str): Session ID

        Returns:
            dict[str, Any] | None: Session data if exist
        """
        raise NotImplementedError

    @abstractmethod
    def session_delete(self, session_id: str) -> None:
        """Delete session.

        Args:
            session_id (str): Session ID
        """
        raise NotImplementedError

    @abstractmethod
    def session_update(self, session_id: str, data: dict[str, Any]) -> None:
        """Update session data.

        Args:
            session_id (str): Session ID
            data (dict[str, Any]): New data
        """
        raise NotImplementedError

    @abstractmethod
    def session_clear(self, session_key: str) -> None:
        """Delete all sessions by key.

        Args:
            session_key (str): Key of session
        """
        raise NotImplementedError

    @abstractmethod
    def session_rework(self, old_session_id: str) -> str:
        """Rework session.

        Args:
            old_session_id (str): Old session id

        Returns:
            str: New session id
        """
        raise NotImplementedError

    @abstractmethod
    def otp_code(
        self, secret: Union[str, bytes], factor: Optional[int] = None
    ) -> str:
        """Generates an OTP.

        Args:
            secret (str | bytes): User secret key.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.

        Returns:
            str: OTP code (fixed-length string).
        """
        raise NotImplementedError

    @abstractmethod
    def otp_uri(
        self,
        secret: str,
        name: Optional[str] = None,
        issuer: Optional[str] = None,
        counter: Optional[int] = None,
    ) -> str:
        """Generates an otpauth:// URI for Google Authenticator.

        Args:
            secret (str): User secret key.
            name (str): Account name (e.g., email).
            issuer (str): Service name (e.g., "GitHub").
            counter (int | None, optional): Counter (for HOTP). Default is None.

        Returns:
            str: A string of the form "otpauth://..."
        """
        raise NotImplementedError

    @abstractmethod
    def otp_verify_code(
        self,
        secret: Union[str, bytes],
        code: str,
        factor: Optional[int] = None,
        look_ahead: Optional[int] = 1,
    ) -> bool:
        """Checks the OTP code, taking into account the acceptable window.

        Args:
            secret (str | bytes): User secret key.
            code (str): The code entered.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.
            look_ahead (int, optional): Acceptable deviation in intervals (±window(totp) / ±look ahead(hotp)). Default is 1.

        Returns:
            bool: True if the code matches, otherwise False.
        """
        raise NotImplementedError

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
