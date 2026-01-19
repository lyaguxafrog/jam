# -*- coding: utf-8 -*-

import datetime
from typing import Any
import uuid

from jam.__base__ import BaseJam


class Jam(BaseJam):
    """Main instance."""

    MODULES: dict[str, str] = {
        "jwt": "jam.jwt.create_instance",
        "session": "jam.sessions.create_instance",
        "oauth2": "jam.oauth2.create_instance",
        "paseto": "jam.paseto.create_instance",
        "otp": "jam.otp.create_instance",
    }

    def jwt_make_payload(
        self, exp: int | None, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Make JWT-specific payload.

        Args:
            exp (int | None): Token expire, if None -> use default
            data (dict[str, Any]): Data to payload

        Returns:
            dict[str, Any]: Payload
        """
        payload = {
            "iat": datetime.datetime.now().timestamp(),
            "exp": (datetime.datetime.now().timestamp() + exp) if exp else None,
            "jti": str(uuid.uuid4()),
        }
        payload = payload | data
        return payload

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
        self._BaseJam__logger.debug(
            f"Creating JWT token with payload keys: {list(payload.keys())}"
        )
        token = self.jwt.encode(payload=payload)
        self._BaseJam__logger.debug(
            f"JWT token created successfully, length: {len(token)} characters"
        )
        return token

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
        self._BaseJam__logger.debug(
            f"Verifying JWT token (length: {len(token)} chars), check_exp={check_exp}, check_list={check_list}"
        )
        payload = self.jwt.decode(token)
        self._BaseJam__logger.debug(
            f"JWT token verified successfully, payload keys: {list(payload.keys())}"
        )
        return payload

    def session_create(self, session_key: str, data: dict[str, Any]) -> str:
        """Create new session.

        Args:
            session_key (str): Key for session
            data (dict[str, Any]): Session data

        Returns:
            str: New session ID
        """
        self._BaseJam__logger.debug(
            f"Creating session with key: {session_key}, data keys: {list(data.keys())}"
        )
        session_id = self.session.create(session_key, data)
        self._BaseJam__logger.debug(
            f"Session created successfully, session_id: {session_id}"
        )
        return session_id

    def session_get(self, session_id: str) -> dict[str, Any] | None:
        """Get data from session.

        Args:
            session_id (str): Session ID

        Returns:
            dict[str, Any] | None: Session data if exist
        """
        self._BaseJam__logger.debug(
            f"Getting session data for session_id: {session_id}"
        )
        data = self.session.get(session_id)
        if data:
            self._BaseJam__logger.debug(
                f"Session data retrieved, keys: {list(data.keys())}"
            )
        else:
            self._BaseJam__logger.debug(f"Session {session_id} not found")
        return data

    def session_delete(self, session_id: str) -> None:
        """Delete session.

        Args:
            session_id (str): Session ID
        """
        return self.session.delete(session_id)

    def session_update(self, session_id: str, data: dict[str, Any]) -> None:
        """Update session data.

        Args:
            session_id (str): Session ID
            data (dict[str, Any]): New data
        """
        return self.session.update(session_id, data)

    def session_clear(self, session_key: str) -> None:
        """Delete all sessions by key.

        Args:
            session_key (str): Key of session
        """
        return self.session.clear(session_key)

    def session_rework(self, old_session_id: str) -> str:
        """Rework session.

        Args:
            old_session_id (str): Old session id

        Returns:
            str: New session id
        """
        return self.session.rework(old_session_id)

    def otp_code(self, secret: str | bytes, factor: int | None = None) -> str:
        """Generates an OTP.

        Args:
            secret (str | bytes): User secret key.
            factor (int | None, optional): Unixtime for TOTP(if none, use now time) / Counter for HOTP.

        Returns:
            str: OTP code (fixed-length string).
        """
        return self.otp(secret=secret).at(factor)

    def otp_uri(
        self,
        secret: str,
        name: str | None = None,
        issuer: str | None = None,
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
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).provisioning_uri(
            name=name, issuer=issuer, type_=self._otp.type, counter=counter
        )

    def otp_verify_code(
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
        self._otp_checker()
        return self._otp_module(
            secret=secret, digits=self._otp.digits, digest=self._otp.digest
        ).verify(code=code, factor=factor, look_ahead=look_ahead)

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
        from jam.exceptions import ProviderNotConfigurError

        if provider not in self.oauth2:
            raise ProviderNotConfigurError(
                f"Provider {provider} not configured"
            )
        return self.oauth2[provider].get_authorization_url(
            scope, **extra_params
        )

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
        from jam.exceptions import ProviderNotConfigurError

        if provider not in self.oauth2:
            raise ProviderNotConfigurError(
                f"Provider {provider} not configured"
            )
        return self.oauth2[provider].fetch_token(
            code, grant_type, **extra_params
        )

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
        from jam.exceptions import ProviderNotConfigurError

        if provider not in self.oauth2:
            raise ProviderNotConfigurError(
                f"Provider {provider} not configured"
            )
        return self.oauth2[provider].refresh_token(
            refresh_token, grant_type, **extra_params
        )

    def oauth2_client_credentials_flow(
        self,
        provider: str,
        scope: list[str] | None = None,
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Obtain access token using client credentials flow (no user interaction).

        Args:
            provider (str): OAuth2 provider
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
        return self.oauth2[provider].client_credentials_flow(
            scope, **extra_params
        )

    def paseto_make_payload(
        self, exp: int | None = None, **data: dict[str, Any]
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

    def paseto_create(
        self,
        payload: dict[str, Any],
        footer: dict[str, Any] | str | None,
    ) -> str:
        """Create new PASETO.

        Args:
            payload (dict[str, Any]): Payload
            footer (dict | str  | None): Footer

        Returns:
            str: New token
        """
        return self.paseto.encode(payload=payload, footer=footer)

    def paseto_decode(
        self, token: str, check_exp: bool = True, check_list: bool = True
    ) -> dict[str, dict[str, Any] | str | None]:
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
