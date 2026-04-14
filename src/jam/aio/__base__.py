# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Any

from jam.__base__ import BaseJam
from jam.aio.oauth2.__base__ import BaseAsyncOAuth2Client
from jam.aio.sessions.__base__ import BaseAsyncSessionModule


class BaseAsyncJam(BaseJam):
    """Base async jam instance."""

    MODULES: dict[str, str] = {}

    session: BaseAsyncSessionModule | None = None  # type: ignore[override]
    oauth2: dict[str, BaseAsyncOAuth2Client] | None = None  # type: ignore[override]

    @abstractmethod
    async def jwt_make_payload(  # type: ignore[override]
        self, exp: int | None, data: dict[str, Any]
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
    async def jwt_create(  # type: ignore[override]
        self, payload: dict[str, Any]
    ) -> str:
        """Create JWT token.

        Args:
            payload (dict[str, Any]): Data payload

        Returns:
            str: New token
        """
        raise NotImplementedError

    @abstractmethod
    async def jwt_encode(
        self,
        iss: str | None = None,
        sub: str | None = None,
        aud: str | None = None,
        exp: int | None = None,
        nbf: int | None = None,
        *,
        payload: dict[str, Any] | None = None,
        header: dict[str, Any] | None = None,
    ) -> str:
        """Encode the JWT with the given expire, header, and payload.

        Args:
            exp (int | None): The expiration time in seconds.
            nbf (int | None): The not-before time in seconds.
            iss (str | None): The issuer.
            sub (str | None): The subject.
            aud (str | None): The audience.
            header (dict[str, Any] | None): The header to include in the JWT.
            payload (dict[str, Any] | None): The payload to include in the JWT.

        Returns:
            str: The encoded JWT.
        """
        raise NotImplementedError

    @abstractmethod
    async def jwt_decode(  # type: ignore[override]
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Any]:
        """Verify and decode JWT token.

        Args:
            token (str): JWT token
            check_exp (bool): Check expire
            check_list (bool): Check white/black list. Docs: https://jam.makridenko.ru/jwt/lists/what/

        Returns:
            dict[str, Any]: Decoded payload

        """
        raise NotImplementedError

    @abstractmethod
    async def session_create(  # type: ignore[override]
        self, session_key: str, data: dict[str, Any]
    ) -> str:
        """Create new session.

        Args:
            session_key (str): Key for session
            data (dict[str, Any]): Session data

        Returns:
            str: New session ID
        """
        raise NotImplementedError

    @abstractmethod
    async def session_get(  # type: ignore[override]
        self, session_id: str
    ) -> dict[str, Any] | None:
        """Get data from session.

        Args:
            session_id (str): Session ID

        Returns:
            dict[str, Any] | None: Session data if exist
        """
        raise NotImplementedError

    @abstractmethod
    async def session_delete(  # type: ignore[override]
        self, session_id: str
    ) -> None:
        """Delete session.

        Args:
            session_id (str): Session ID
        """
        raise NotImplementedError

    @abstractmethod
    async def session_update(  # type: ignore[override]
        self, session_id: str, data: dict[str, Any]
    ) -> None:
        """Update session data.

        Args:
            session_id (str): Session ID
            data (dict[str, Any]): New data
        """
        raise NotImplementedError

    @abstractmethod
    async def session_clear(  # type: ignore[override]
        self, session_key: str
    ) -> None:
        """Delete all sessions by key.

        Args:
            session_key (str): Key of session
        """
        raise NotImplementedError

    @abstractmethod
    async def session_rework(  # type: ignore[override]
        self, old_session_id: str
    ) -> str:
        """Rework session.

        Args:
            old_session_id (str): Old session id

        Returns:
            str: New session id
        """
        raise NotImplementedError

    @abstractmethod
    async def otp_code(  # type: ignore[override]
        self, secret: str | bytes, factor: int | None = None
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
    async def otp_uri(  # type: ignore[override]
        self,
        secret: str,
        name: str,
        issuer: str,
        counter: int | None = None,
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
    async def otp_verify_code(  # type: ignore[override]
        self,
        secret: str | bytes,
        code: str,
        factor: int | None = None,
        look_ahead: int | None = 1,
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
    async def oauth2_get_authorized_url(  # type: ignore[override]
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
    async def oauth2_fetch_token(  # type: ignore[override]
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
    async def oauth2_refresh_token(  # type: ignore[override]
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
    async def oauth2_client_credentials_flow(  # type: ignore[override]
        self,
        provider: str,
        scope: list[str] | None = None,
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

    @abstractmethod
    async def paseto_make_payload(  # type: ignore[override]
        self, exp: int | None = None, **data: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate payload for PASETO.

        Args:
            exp (int | None): Custom expire if needed
            data (dict[str, Any]): Data in payload

        Returns:
            dict[str, Any]: New payload
        """
        raise NotImplementedError

    @abstractmethod
    async def paseto_create(  # type: ignore[override]
        self,
        payload: dict[str, Any],
        footer: dict[str, Any] | str | None,
    ) -> str:
        """Create new PASETO.

        Args:
            payload (dict[str, Any]): Payload
            footer (dict[str, Any] | str | None): Payload if needed

        Returns:
            str: PASETO
        """
        raise NotImplementedError

    @abstractmethod
    async def paseto_decode(  # type: ignore[override]
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, dict | str | dict | None]:
        """Decode PASETO and return payload and footer.

        Args:
            token (str): PASETO
            check_exp (bool): Check exp in payload
            check_list (bool): Check token in list

        Returns:
            dict: {`payload`: PAYLOAD, `footer`: FOOTER}
        """
        raise NotImplementedError
