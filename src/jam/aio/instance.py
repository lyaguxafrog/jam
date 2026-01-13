# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Optional, Union
import uuid

from jam.__base__ import BaseJam


class Jam(BaseJam):
    """Main instance for aio."""

    MODULES: dict[str, str] = {
        "jwt": "jam.jwt.create_instance",
        "session": "jam.aio.sessions.create_instance",
        "oauth2": "jam.aio.oauth2.create_instance",
        "paseto": "jam.paseto.create_instance",
    }

    async def jwt_make_payload(
        self, exp: Optional[int], data: dict[str, Any]
    ) -> dict[str, Any]:
        """Make JWT-specific payload.

        Args:
            exp (int | None): Token expire, if None -> use default
            data (dict[str, Any]): Data to payload

        Returns:
            dict[str, Any]: Payload
        """
        payload = {
            "iat": datetime.now().timestamp(),
            "exp": (datetime.now().timestamp() + exp) if exp else None,
            "jti": str(uuid.uuid4()),
        }
        payload = payload | data
        return payload

    async def jwt_create_token(self, payload: dict[str, Any]) -> str:
        """Create JWT token.

        Args:
            payload (dict[str, Any]): Data payload

        Returns:
            str: New token

        Raises:
            EmptySecretKey: If the HMAC algorithm is selected, but the secret key is None
            EmtpyPrivateKey: If RSA algorithm is selected, but private key None
        """
        return self.jwt.encode(payload=payload)

    async def jwt_verify_token(
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
        return self.jwt.decode(token)

    async def session_create(
        self, session_key: str, data: dict[str, Any]
    ) -> str:
        """Create new session.

        Args:
            session_key (str): Key for session
            data (dict[str, Any]): Session data

        Returns:
            str: New session ID
        """
        return await self.session.create(session_key, data)

    async def session_get(self, session_id: str) -> Optional[dict[str, Any]]:
        """Get data from session.

        Args:
            session_id (str): Session ID

        Returns:
            dict[str, Any] | None: Session data if exist
        """
        return await self.session.get(session_id)

    async def session_delete(self, session_id: str) -> None:
        """Delete session.

        Args:
            session_id (str): Session ID
        """
        return await self.session.delete(session_id)

    async def session_update(
        self, session_id: str, data: dict[str, Any]
    ) -> None:
        """Update session data.

        Args:
            session_id (str): Session ID
            data (dict[str, Any]): New data
        """
        return await self.session.update(session_id, data)

    async def session_clear(self, session_key: str) -> None:
        """Delete all sessions by key.

        Args:
            session_key (str): Key of session
        """
        return await self.session.clear(session_key)

    async def session_rework(self, old_session_id: str) -> str:
        """Rework session.

        Args:
            old_session_id (str): Old session id

        Returns:
            str: New session id
        """
        return await self.session.rework(old_session_id)

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
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).at(factor)

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
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).provisioning_uri(
            name=name, issuer=issuer, type_=self._otp.type, counter=counter
        )

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
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).verify(code=code, factor=factor, look_ahead=look_ahead)

    async def oauth2_get_authorized_url(
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
        from jam.exceptions import ProviderNotConfigurError

        if provider not in self.oauth2:
            raise ProviderNotConfigurError(
                f"Provider {provider} not configured"
            )
        return await self.oauth2[provider].get_authorization_url(
            scope, **extra_params
        )

    async def oauth2_fetch_token(
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
        from jam.exceptions import ProviderNotConfigurError

        if provider not in self.oauth2:
            raise ProviderNotConfigurError(
                f"Provider {provider} not configured"
            )
        return await self.oauth2[provider].fetch_token(
            code, grant_type, **extra_params
        )

    async def oauth2_refresh_token(
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
        from jam.exceptions import ProviderNotConfigurError

        if provider not in self.oauth2:
            raise ProviderNotConfigurError(
                f"Provider {provider} not configured"
            )
        return await self.oauth2[provider].refresh_token(
            refresh_token, grant_type, **extra_params
        )

    async def oauth2_client_credentials_flow(
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
        from jam.exceptions import ProviderNotConfigurError

        if provider not in self.oauth2:
            raise ProviderNotConfigurError(
                f"Provider {provider} not configured"
            )
        return await self.oauth2[provider].client_credentials_flow(
            scope, **extra_params
        )

    async def paseto_make_payload(
        self, exp: Optional[int] = None, **data: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate payload for PASETO.

        Args:
            exp (int | None): Token expire
            data (dict[str, Any]): Custom data

        Returns:
            dict: Payload
        """
        from jam.paseto.utils import payload_maker

        return payload_maker(expire=exp, data=data)

    async def paseto_create(
        self,
        payload: dict[str, Any],
        footer: Optional[Union[dict[str, Any], str]],
    ) -> str:
        """Create new PASETO.

        Args:
            payload (dict[str, Any]): Payload
            footer (dict | str  | None): Footer

        Returns:
            str: New token
        """
        return self.paseto.encode(payload=payload, footer=footer)

    async def paseto_decode(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, Union[dict, Union[str, dict, None]]]:
        """Decode PASETO.

        Args:
            token (str): Token
            check_exp (bool): Check exp in payload
            check_list (bool): Check token in list

        Returns:
            dict: {'payload' PAYLOAD, 'footer': FOOTER}
        """
        payload, footer = self.paseto.decode(token)
        return {"payload": payload, "footer": footer}
